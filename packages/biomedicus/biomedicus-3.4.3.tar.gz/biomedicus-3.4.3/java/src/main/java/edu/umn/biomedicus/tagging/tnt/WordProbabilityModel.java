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

package edu.umn.biomedicus.tagging.tnt;

import edu.umn.biomedicus.common.tuples.WordCap;
import edu.umn.biomedicus.common.tuples.WordPosCap;
import edu.umn.biomedicus.common.pos.PartOfSpeech;

import java.util.Set;

/**
 * Interface for word probability models.
 *
 * @since 1.7.0
 */
public interface WordProbabilityModel {


  /**
   * Convenience method for #logProbabilityOfWord(edu.umn.biomedicus.syntax.tnt.models.WordPosCap).
   * Constructs a new {@link WordPosCap} from the arguments.
   *
   * @param candidate the conditional PartOfSpeech
   * @return a negative double representing the log10 probability of the word
   */
  double logProbabilityOfWord(PartOfSpeech candidate, WordCap wordCap);

  /**
   * Returns the potential part of speech candidates for a given word
   *
   * @return a set of {@link PartOfSpeech} enum values
   */
  Set<PartOfSpeech> getCandidates(WordCap wordCap);

  /**
   * Given a word, returns if this model can account for its probability.
   *
   * @return true if this model can provide a probability for the word, false otherwise
   */
  boolean isKnown(WordCap wordCap);

  void createDataStore(DataStoreFactory dataStoreFactory);

  /**
   * Loads the data from a map db database.
   *
   * @param dataStoreFactory factory for creating the known words data store.
   */
  void openDataStore(DataStoreFactory dataStoreFactory);

  /**
   * Writes the data to a MapDB database.
   *
   */
  void writeData();

  /**
   * Gets the identifier for this word probability model
   *
   * @return integer identifier
   */
  int getId();

  /**
   * Sets the integer identifier for this word probability model.
   *
   * @param id integer identifier
   */
  void setId(int id);
}
