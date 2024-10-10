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

package edu.umn.biomedicus.common.tuples;

import org.jetbrains.annotations.NotNull;
import java.io.Serializable;
import java.util.function.BiConsumer;

/**
 * A 2-tuple, sequence of two objects, of different or the same type.
 * The two objects should not be null.
 *
 * @param <T> Type of the first object
 * @param <U> Type of the second object
 */
public class Pair<T, U> implements Serializable {

  private final T first;

  private final U second;

  /**
   * Creates a Pair with the passed arguments. Passing null objects will break
   * this class.
   *
   * @param first a non-null first object.
   * @param second a non-null second object.
   */
  public Pair(@NotNull T first, @NotNull U second) {
    this.first = first;
    this.second = second;
  }

  /**
   * Creates a Pair with the passed arguments. Passing null objects will break
   * this class.
   *
   * @param first a non-null first object.
   * @param second a non-null second object.
   */
  public static <T, U> Pair<T, U> of(T first, U second) {
    return new Pair<>(first, second);
  }

  @NotNull
  public T getFirst() {
    return first;
  }

  @NotNull
  public T first() {
    return first;
  }

  @NotNull
  public U getSecond() {
    return second;
  }

  @NotNull
  public U second() {
    return second;
  }

  /**
   * Swaps the two elements of the pair and returns the result.
   *
   * @return newly created pair of the elements of this pair swapped.
   */
  public Pair<U, T> swap() {
    return new Pair<>(second, first);
  }

  /**
   * Calls the BiFunction on the two elements of this Pair.
   *
   * @param function function to call
   */
  public void call(BiConsumer<T, U> function) {
    function.accept(first, second);
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }

    Pair<?, ?> pair = (Pair<?, ?>) o;

    if (!first.equals(pair.first)) {
      return false;
    }
    return second.equals(pair.second);

  }

  @Override
  public int hashCode() {
    int result = first.hashCode();
    result = 31 * result + second.hashCode();
    return result;
  }
}
