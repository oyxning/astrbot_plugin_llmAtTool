## 插件信息

- **插件名称**：llm_at_tool_plugin
- **作者**：LumineStory
- **仓库地址**：[https://github.com/oyxning/astrbot_plugin_llmAtTool](https://github.com/oyxning/astrbot_plugin_llmAtTool)
- **描述**：提供一个可供LLM调用的@用户工具(Tool)

## 功能简介

本插件为 AstrBot 提供了一个 LLM 函数调用（Function Calling）能力的 @用户工具。允许 LLM 根据对话上下文，智能地决定何时以及如何 @ 一个指定的用户。

- 支持通过工具函数 at_user 实现智能 @ 指定用户并发送消息
- 可配置是否启用工具、@消息前缀等参数
- 详细日志输出，便于调试和维护

## 使用方法

1. 将本插件放入 AstrBot 插件目录。
2. 按需修改 `_conf_schema.json` 配置文件，设置 `enable_at_tool`、`at_prefix_message` 等参数。
3. 启动 AstrBot，插件会自动加载。

### 工具函数 at_user

- **参数**：
  - `user_id` (string)：需要@的用户唯一ID（如QQ号，必须为纯数字）
  - `message` (string)：@用户后发送的文本消息
- **返回**：@指定用户并发送消息

## 配置项说明

- `enable_at_tool`：是否启用@用户工具（布尔值，默认启用）
- `at_prefix_message`：@消息的前缀文本（字符串，可选）

## 支持

[帮助文档](https://astrbot.app)
