/*-------------------------------------------------------------------------
 * Copyright (c) Microsoft Corporation.  All rights reserved.
 *
 * include/utils/pcre_regex.h
 *
 * Utilities for PCRE Regex evaluation
 *
 *-------------------------------------------------------------------------
 */

#ifndef PCRE_REGEX_H
#define PCRE_REGEX_H


struct PcreData;

void RegexCompileDuringPlanning(char *regexPatternStr, char *options);
struct PcreData * RegexCompile(char *regexPatternStr, char *options);
struct PcreData * RegexCompileForAggregation(char *regexPatternStr, char *options,
									  bool enableNoAutoCapture,
									  const char *regexInvalidErrorMessage);
size_t * GetResultVectorUsingPcreData(struct PcreData *pcreData);
int GetResultLengthUsingPcreData(struct PcreData *pcreData);
bool IsValidRegexOptions(char *options);
void FreePcreData(struct PcreData *pcreData);

bool PcreRegexExecute(char *regexPatternStr, char *options,
					  struct PcreData *pcreData,
					  const StringView *subjectString);

#endif
