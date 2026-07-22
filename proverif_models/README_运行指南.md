# 符号模型运行指南：当前证据边界

本目录中的 M1-M6 是工具特定的示例性骨架，不是六个协议族的忠实实现，也不是同一协议在多个工具之间的语义翻译。

- M1 的权威 ProVerif 状态为 PARTIAL：诚实完成、保密性和响应方注入一致性通过；发起方注入一致性在 120 秒时超时。
- M2-M6 的 ProVerif 结果仅说明所编码查询的运行情况。
- 全部 Tamarin 和 Scyther 家族文件仅为示例性执行，不能据此给出跨工具或算法级结论。
- M3 的 fresh-atom lemma 不是有效的 PFS 测试。
- AVISPA 未在本地执行。

运行前请先阅读 `MODEL_SCOPE_AND_CORRECTION_NOTICE.md` 和
`supplement_S3_logs/S3_MODEL_VALIDITY_STATUS.csv`。工具输出中的 PASS 只适用于对应的编码查询，不能自动推广为协议实现、机制族或部署系统的安全结论。

已发表协议的有界诊断使用 C1-C3 命名空间：C1=CCAP、C2=CL-BASA、C3=BCAE。性能组合使用独立的 Perf-P1 命名空间；论文正文中的短标签 P1 指 Perf-P1。
