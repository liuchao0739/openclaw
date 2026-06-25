# Spec: infra/logging

## 源文件
- `src/logging/` 目录下核心模块
- 优先：`src/logging/logger.ts`, `src/logging/format.ts`

## 目标文件
- `openclaw/infra/logging.py`
- `tests/test_infra_logging.py`

## 技术选型
- 使用 `structlog` 替代 TS 自定义 logger

## 验收
- 支持 log level 环境变量控制
- 结构化 JSON / 人类可读两种格式
- gateway 启动时能输出 startup trace 级别日志
