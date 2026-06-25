# 循环执行指令（单行，避免 JSON 换行错误）

从 migration/progress.json 读取 status=pending 的第一个 task，按 task 的 spec 文件完成 Python 实现，写测试，更新 progress.json 为 done，git commit，然后继续下一个 pending task；若全部 done 则输出 MIGRATION_COMPLETE。
