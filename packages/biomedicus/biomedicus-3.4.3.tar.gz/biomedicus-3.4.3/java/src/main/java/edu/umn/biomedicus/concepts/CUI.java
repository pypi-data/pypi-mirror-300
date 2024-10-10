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

package edu.umn.biomedicus.concepts;

import org.jetbrains.annotations.Nullable;
import java.io.Serializable;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 *
 */
public class CUI implements Serializable {

  public static final Pattern CUI_PATTERN = Pattern.compile("C([\\d]{7})");

  private final int identifier;

  public CUI(int identifier) {
    this.identifier = identifier;
  }

  public CUI(String wordForm) {
    Matcher matcher = CUI_PATTERN.matcher(wordForm);
    if (matcher.find()) {
      String identifier = matcher.group(1);
      this.identifier = Integer.parseInt(identifier);
    } else {
      throw new IllegalArgumentException("Word form does not match CUI pattern");
    }
  }

  @Override
  public boolean equals(@Nullable Object o) {
    if (this == o) {
      return true;
    }
    if (o == null || getClass() != o.getClass()) {
      return false;
    }

    CUI cui = (CUI) o;

    return identifier == cui.identifier;
  }

  @Override
  public int hashCode() {
    return identifier;
  }

  @Override
  public String toString() {
    return String.format("C%07d", identifier);
  }

  public int identifier() {
    return identifier;
  }
}
