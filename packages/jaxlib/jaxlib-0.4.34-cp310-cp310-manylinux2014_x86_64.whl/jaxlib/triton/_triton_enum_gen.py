# pytype: skip-file

# Autogenerated by mlir-tblgen; don't manually edit.

from enum import IntEnum, auto, IntFlag
from jaxlib.mlir.dialects._ods_common import _cext as _ods_cext
from jaxlib.mlir.ir import register_attribute_builder
_ods_ir = _ods_cext.ir

class RMWOp(IntEnum):
    """allowed 32-bit signless integer cases: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10"""

    AND = 1
    OR = 2
    XOR = 3
    ADD = 4
    FADD = 5
    MAX = 6
    MIN = 7
    UMAX = 8
    UMIN = 9
    XCHG = 10

    def __str__(self):
        if self is RMWOp.AND:
            return "and"
        if self is RMWOp.OR:
            return "or"
        if self is RMWOp.XOR:
            return "xor"
        if self is RMWOp.ADD:
            return "add"
        if self is RMWOp.FADD:
            return "fadd"
        if self is RMWOp.MAX:
            return "max"
        if self is RMWOp.MIN:
            return "min"
        if self is RMWOp.UMAX:
            return "umax"
        if self is RMWOp.UMIN:
            return "umin"
        if self is RMWOp.XCHG:
            return "exch"
        raise ValueError("Unknown RMWOp enum entry.")



@register_attribute_builder("TT_AtomicRMWAttr")
def _tt_atomicrmwattr(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(32, context=context), int(x))

class CacheModifier(IntEnum):
    """allowed 32-bit signless integer cases: 1, 2, 3, 4, 5, 6, 7"""

    NONE = 1
    CA = 2
    CG = 3
    WB = 4
    CS = 5
    WT = 6
    CV = 7

    def __str__(self):
        if self is CacheModifier.NONE:
            return "none"
        if self is CacheModifier.CA:
            return "ca"
        if self is CacheModifier.CG:
            return "cg"
        if self is CacheModifier.WB:
            return "wb"
        if self is CacheModifier.CS:
            return "cs"
        if self is CacheModifier.WT:
            return "wt"
        if self is CacheModifier.CV:
            return "cv"
        raise ValueError("Unknown CacheModifier enum entry.")



@register_attribute_builder("TT_CacheModifierAttr")
def _tt_cachemodifierattr(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(32, context=context), int(x))

class EvictionPolicy(IntEnum):
    """allowed 32-bit signless integer cases: 1, 2, 3"""

    NORMAL = 1
    EVICT_FIRST = 2
    EVICT_LAST = 3

    def __str__(self):
        if self is EvictionPolicy.NORMAL:
            return "evict_normal"
        if self is EvictionPolicy.EVICT_FIRST:
            return "evict_first"
        if self is EvictionPolicy.EVICT_LAST:
            return "evict_last"
        raise ValueError("Unknown EvictionPolicy enum entry.")



@register_attribute_builder("TT_EvictionPolicyAttr")
def _tt_evictionpolicyattr(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(32, context=context), int(x))

class InputPrecision(IntEnum):
    """allowed 32-bit signless integer cases: 0, 1, 2"""

    TF32 = 0
    TF32x3 = 1
    IEEE = 2

    def __str__(self):
        if self is InputPrecision.TF32:
            return "tf32"
        if self is InputPrecision.TF32x3:
            return "tf32x3"
        if self is InputPrecision.IEEE:
            return "ieee"
        raise ValueError("Unknown InputPrecision enum entry.")



@register_attribute_builder("TT_InputPrecisionAttr")
def _tt_inputprecisionattr(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(32, context=context), int(x))

class MemSemantic(IntEnum):
    """allowed 32-bit signless integer cases: 1, 2, 3, 4"""

    RELAXED = 1
    ACQUIRE = 2
    RELEASE = 3
    ACQUIRE_RELEASE = 4

    def __str__(self):
        if self is MemSemantic.RELAXED:
            return "relaxed"
        if self is MemSemantic.ACQUIRE:
            return "acquire"
        if self is MemSemantic.RELEASE:
            return "release"
        if self is MemSemantic.ACQUIRE_RELEASE:
            return "acq_rel"
        raise ValueError("Unknown MemSemantic enum entry.")



@register_attribute_builder("TT_MemSemanticAttr")
def _tt_memsemanticattr(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(32, context=context), int(x))

class MemSyncScope(IntEnum):
    """allowed 32-bit signless integer cases: 1, 2, 3"""

    GPU = 1
    CTA = 2
    SYSTEM = 3

    def __str__(self):
        if self is MemSyncScope.GPU:
            return "gpu"
        if self is MemSyncScope.CTA:
            return "cta"
        if self is MemSyncScope.SYSTEM:
            return "sys"
        raise ValueError("Unknown MemSyncScope enum entry.")



@register_attribute_builder("TT_MemSyncScopeAttr")
def _tt_memsyncscopeattr(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(32, context=context), int(x))

class PaddingOption(IntEnum):
    """allowed 32-bit signless integer cases: 1, 2"""

    PAD_ZERO = 1
    PAD_NAN = 2

    def __str__(self):
        if self is PaddingOption.PAD_ZERO:
            return "zero"
        if self is PaddingOption.PAD_NAN:
            return "nan"
        raise ValueError("Unknown PaddingOption enum entry.")



@register_attribute_builder("TT_PaddingOptionAttr")
def _tt_paddingoptionattr(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(32, context=context), int(x))

class ProgramIDDim(IntEnum):
    """allowed 32-bit signless integer cases: 0, 1, 2"""

    X = 0
    Y = 1
    Z = 2

    def __str__(self):
        if self is ProgramIDDim.X:
            return "x"
        if self is ProgramIDDim.Y:
            return "y"
        if self is ProgramIDDim.Z:
            return "z"
        raise ValueError("Unknown ProgramIDDim enum entry.")



@register_attribute_builder("TT_ProgramDim")
def _tt_programdim(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(32, context=context), int(x))

class PropagateNan(IntEnum):
    """allowed 32-bit signless integer cases: 0, 65535"""

    NONE = 0
    ALL = 65535

    def __str__(self):
        if self is PropagateNan.NONE:
            return "none"
        if self is PropagateNan.ALL:
            return "all"
        raise ValueError("Unknown PropagateNan enum entry.")



@register_attribute_builder("TT_PropagateNanAttr")
def _tt_propagatenanattr(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(32, context=context), int(x))

class RoundingMode(IntEnum):
    """allowed 32-bit signless integer cases: 0, 1"""

    RTZ = 0
    RTNE = 1

    def __str__(self):
        if self is RoundingMode.RTZ:
            return "rtz"
        if self is RoundingMode.RTNE:
            return "rtne"
        raise ValueError("Unknown RoundingMode enum entry.")



@register_attribute_builder("TT_RoundingModeAttr")
def _tt_roundingmodeattr(x, context):
    return _ods_ir.IntegerAttr.get(_ods_ir.IntegerType.get_signless(32, context=context), int(x))

