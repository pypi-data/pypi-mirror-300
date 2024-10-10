/*
 * Copyright 2019 Regents of the University of Minnesota.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

package edu.umn.biomedicus.acronym;

import org.jetbrains.annotations.Nullable;
import org.rocksdb.*;

import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.*;

public class RocksDBSenseVectors implements SenseVectors {

  private final RocksDB rocksDB;

  private transient int _size = -1;

  public RocksDBSenseVectors(Path path, boolean forWriting) {
    RocksDB.loadLibrary();

    if (forWriting) {
      try (Options options = new Options()) {
        options.setCreateIfMissing(true);
        options.prepareForBulkLoad();
        rocksDB = RocksDB.open(options, path.toString());
      } catch (RocksDBException e) {
        throw new RuntimeException(e);
      }
    } else {
      try {
        rocksDB = RocksDB.openReadOnly(path.toString());
      } catch (RocksDBException e) {
        throw new RuntimeException(e);
      }
    }
  }

  @Override
  public boolean containsSense(@Nullable String sense) {
    if (sense == null) {
      return false;
    }

    byte[] bytes = sense.getBytes(StandardCharsets.UTF_8);
    try {
      byte[] value = rocksDB.get(bytes);
      return value != null;
    } catch (RocksDBException e) {
      throw new RuntimeException(e);
    }
  }

  @Nullable
  @Override
  public SparseVector get(@Nullable String sense) {
    if (sense == null) {
      return null;
    }

    byte[] bytes = sense.getBytes(StandardCharsets.UTF_8);
    try {
      byte[] value = rocksDB.get(bytes);
      return new SparseVector(value);
    } catch (RocksDBException e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  public void removeWord(int index) {
    try (WriteBatch writeBatch = new WriteBatch()) {
      try (RocksIterator rocksIterator = rocksDB.newIterator()) {
        rocksIterator.seekToFirst();
        while (rocksIterator.isValid()) {
          SparseVector sparseVector = new SparseVector(rocksIterator.value());
          sparseVector.remove(index);
          writeBatch.put(rocksIterator.key(), sparseVector.toBytes());
        }
      }
      rocksDB.write(new WriteOptions(), writeBatch);
    } catch (RocksDBException e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  public void removeWords(Collection<Integer> indexes) {
    try (WriteBatch writeBatch = new WriteBatch()) {
      try (RocksIterator rocksIterator = rocksDB.newIterator()) {
        rocksIterator.seekToFirst();
        while (rocksIterator.isValid()) {
          SparseVector sparseVector = new SparseVector(rocksIterator.value());
          sparseVector.removeAll(indexes);
          writeBatch.put(rocksIterator.key(), sparseVector.toBytes());
        }
      }
      rocksDB.write(new WriteOptions(), writeBatch);
    } catch (RocksDBException e) {
      throw new RuntimeException(e);
    }
  }

  @Override
  public int size() {
    int size = _size;
    if (size != -1) {
      return size;
    }

    size = 0;
    try (RocksIterator rocksIterator = rocksDB.newIterator()) {
      rocksIterator.seekToFirst();
      while (rocksIterator.isValid()) {
        size++;
        rocksIterator.next();
      }
    }

    return (_size = size);
  }

  @Override
  public void close() {
    rocksDB.close();
  }

  public SenseVectors inMemory(@Nullable Boolean sensesInMemory) {
    if (sensesInMemory != null && sensesInMemory) {
      Map<String, SparseVector> map = new HashMap<>(size());
      try (RocksIterator rocksIterator = rocksDB.newIterator()) {
        rocksIterator.seekToFirst();
        while (rocksIterator.isValid()) {
          map.put(new String(rocksIterator.key(), StandardCharsets.UTF_8),
              new SparseVector(rocksIterator.value()));
          rocksIterator.next();
        }
      }
      rocksDB.close();
      return new HashSenseVectors(map);
    }
    return this;
  }

  void putAll(Map<String, SparseVector> map) {
    map.forEach((key, value) -> {
      try {
        rocksDB.put(key.getBytes(StandardCharsets.UTF_8), value.toBytes());
      } catch (RocksDBException e) {
        throw new RuntimeException(e);
      }
    });
  }
}
