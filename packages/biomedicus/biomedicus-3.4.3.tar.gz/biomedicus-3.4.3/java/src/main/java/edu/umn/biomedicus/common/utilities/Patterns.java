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

package edu.umn.biomedicus.common.utilities;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

/**
 *
 */
public final class Patterns {

  /**
   * A Pattern that will match against any character that is not whitespace. <p> Using {@link
   * java.util.regex.Matcher#find} will return whether or not a string has any non-whitespace
   * characters.
   */
  public static final Pattern NON_WHITESPACE = Pattern.compile("\\S");
  /**
   * A Pattern that will match against a string that only contains one or more unicode alphabetic
   * characters.
   */
  public static final Pattern ALPHABETIC_WORD = Pattern
      .compile("[\\p{L}]+");
  /**
   * A pattern that will match against a string that only contains one or more unicode alphanumeric
   * characters.
   */
  public static final Pattern ALPHANUMERIC_WORD = Pattern
      .compile("[\\p{L}\\p{Nd}]+");
  /**
   * A pattern that will match any unicode alphanumeric character
   */
  public static final Pattern A_LETTER_OR_NUMBER = Pattern
      .compile("[\\p{Nd}\\p{L}]");
  /**
   * A pattern that will match the newline character.
   */
  public static final Pattern NEWLINE = Pattern.compile("\n");

  public static final Pattern INITIAL_WHITESPACE = Pattern.compile("^\\s+");

  public static final Pattern FINAL_WHITESPACE = Pattern.compile("\\s+$");

  /**
   * Private constructor to prevent instantiation of utility class.
   */
  private Patterns() {
    throw new UnsupportedOperationException();
  }

  /**
   * Loads a pattern from a file in the resource path by joining all of the lines of the file with
   * an OR symbol '|'
   *
   * @param resourceName the path to the resource of regex statements to be joined
   * @return newly created pattern
   * @throws IOException if there is a failure finding or reading the file.
   */
  public static Pattern loadPatternByJoiningLines(String resourceName) throws IOException {
    InputStream is = Thread.currentThread().getContextClassLoader().getResourceAsStream(resourceName);
    if (is == null) {
      throw new FileNotFoundException();
    }
    try (BufferedReader reader = new BufferedReader(new InputStreamReader(is))) {
      return getPattern(reader);
    }
  }

  private static Pattern getPattern(BufferedReader reader) {
    return Pattern
        .compile(reader.lines().collect(Collectors.joining("|")),
            Pattern.MULTILINE | Pattern.UNIX_LINES);
  }

  public static Pattern loadPatternByJoiningLines(Path path) throws IOException {
    try (BufferedReader reader = Files.newBufferedReader(path)) {
      return getPattern(reader);
    }
  }
}
