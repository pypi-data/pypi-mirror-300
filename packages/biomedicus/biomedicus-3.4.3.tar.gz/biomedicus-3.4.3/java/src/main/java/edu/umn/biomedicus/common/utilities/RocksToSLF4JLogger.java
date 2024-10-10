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

import org.rocksdb.InfoLogLevel;
import org.rocksdb.Logger;

public class RocksToSLF4JLogger extends Logger {

  private final org.slf4j.Logger slf4jLogger;

  public RocksToSLF4JLogger(InfoLogLevel logLevel, org.slf4j.Logger slf4jLogger) {
    super(logLevel);
    this.slf4jLogger = slf4jLogger;
  }

  @Override
  protected void log(InfoLogLevel infoLogLevel, String logMsg) {
    switch (infoLogLevel) {
      case DEBUG_LEVEL:
        slf4jLogger.debug(logMsg);
        break;
      case INFO_LEVEL:
        slf4jLogger.info(logMsg);
        break;
      case WARN_LEVEL:
        slf4jLogger.warn(logMsg);
        break;
      case ERROR_LEVEL:
      case FATAL_LEVEL:
      case HEADER_LEVEL:
      case NUM_INFO_LOG_LEVELS:
        slf4jLogger.error(logMsg);
        break;
    }
  }
}
