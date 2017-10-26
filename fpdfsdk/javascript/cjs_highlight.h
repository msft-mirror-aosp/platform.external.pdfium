// Copyright 2017 PDFium Authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Original code copyright 2014 Foxit Software Inc. http://www.foxitsoftware.com

#ifndef FPDFSDK_JAVASCRIPT_CJS_HIGHLIGHT_H_
#define FPDFSDK_JAVASCRIPT_CJS_HIGHLIGHT_H_

#include "fpdfsdk/javascript/JS_Define.h"

class CJS_Highlight : public CJS_Object {
 public:
  explicit CJS_Highlight(v8::Local<v8::Object> pObject) : CJS_Object(pObject) {}
  ~CJS_Highlight() override {}

  static const char* g_pClassName;
  static int g_nObjDefnID;
  static void DefineJSObjects(CFXJS_Engine* pEngine, FXJSOBJTYPE eObjType);

  static JSConstSpec ConstSpecs[];
  static void DefineConsts(CFXJS_Engine* pEngine);
};

#endif  // FPDFSDK_JAVASCRIPT_CJS_HIGHLIGHT_H_
