// Copyright 2017 The PDFium Authors
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

// Original code copyright 2014 Foxit Software Inc. http://www.foxitsoftware.com

#include "xfa/fxfa/parser/cxfa_era.h"

#include "fxjs/xfa/cjx_node.h"
#include "xfa/fxfa/parser/cxfa_document.h"

CXFA_Era::CXFA_Era(CXFA_Document* doc, XFA_PacketType packet)
    : CXFA_Node(doc,
                packet,
                XFA_XDPPACKET::kLocaleSet,
                XFA_ObjectType::ContentNode,
                XFA_Element::Era,
                {},
                {},
                cppgc::MakeGarbageCollected<CJX_Node>(
                    doc->GetHeap()->GetAllocationHandle(),
                    this)) {}

CXFA_Era::~CXFA_Era() = default;
