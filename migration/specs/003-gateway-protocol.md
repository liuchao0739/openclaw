# Spec: gateway-protocol

## 源目录
- `packages/gateway-protocol/src/`

## 目标目录
- `openclaw/protocol/`

## 优先文件
1. `version.ts` → `version.py`
2. `client-info.ts` → `client_info.py`
3. `connect-error-details.ts` → `connect_error_details.py`
4. `startup-unavailable.ts` → `startup_unavailable.py`
5. `schema.ts` + `schema/` → `schema.py` + `schema/`

## 技术选型
- TypeBox schema → Pydantic v2 models
- 保持 protocol version 常量一致

## 验收
- 所有 schema 可序列化/反序列化
- 移植 `index.test.ts` 中的核心断言
- `PROTOCOL_VERSION` 与 TS 版相同
