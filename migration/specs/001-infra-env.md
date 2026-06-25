# Spec: infra/env

## 源文件
- `src/infra/env.ts`
- `src/infra/env.test.ts` (如有)

## 目标文件
- `openclaw/infra/env.py`
- `tests/test_infra_env.py`

## 需移植的函数
- `is_truthy_env_value(value) -> bool`
- `normalize_env() -> None`
- `is_vitest_runtime_env(env) -> bool` → 改为 `is_pytest_runtime_env`
- `resolve_env_normalization_keys(key) -> list[str]`
- `expand_env_normalization_keys(keys) -> set[str]`
- `normalize_zai_env(env) -> None`

## 验收
- pytest 覆盖所有公开函数
- `OPENCLAW_*` 环境变量规范化行为与 TS 版一致
- `is_truthy_env_value` 对 `1`, `true`, `yes`, `on` 返回 True
