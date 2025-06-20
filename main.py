# main.py
# 导入所有必要的模块
import astrbot.api.message_components as Comp
from astrbot.api import AstrBotConfig, logger
from astrbot.api.event import AstrMessageEvent, MessageEventResult, filter
from astrbot.api.star import Context, Star, register


@register(
    "llm_at_tool_plugin",  # 插件名称
    "LumineStory",            # 插件作者
    "提供一个可供LLM调用的@用户工具(Tool)",  # 插件描述
    "1.0.0",               # 插件版本
    "https://github.com/oyxning/astrbot_plugin_llmAtTool" # 插件仓库地址
)
class LlmAtToolPlugin(Star):
    """
    一个实现了LLM函数调用(Function Calling)的@用户工具插件。
    允许LLM根据对话上下文，智能地决定何时以及如何@一个指定的用户。
    """

    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        
        # 将传入的config对象保存为实例属性，以便在插件的其他方法中使用
        self.config = config
        
        # 使用 self.config.get() 方法安全地读取配置项，如果用户未配置则使用默认值
        self.is_tool_enabled = self.config.get("enable_at_tool", True)
        self.at_prefix = self.config.get("at_prefix_message", "")
        
        # 在日志中打印加载的配置，方便调试
        logger.info("LLM @用户工具插件已加载。")
        logger.info(f" - 工具启用状态: {self.is_tool_enabled}")
        logger.info(f" - @消息前缀: '{self.at_prefix}'")
        
        if not self.is_tool_enabled:
            logger.warning("LLM @用户工具当前已被禁用，将不会注册函数工具。")

    @filter.llm_tool(name="at_user")
    async def at_user_tool(self, event: AstrMessageEvent, user_id: str, message: str) -> MessageEventResult:
        """
        当需要特别提醒或提及某位用户时，调用此工具来@他们并发送一条消息。
        Args:
            user_id (string): 需要@的用户的唯一ID（例如QQ号）。
            message (string): 需要在@用户后发送的文本消息。
        """
        # 每次调用工具时，都检查配置中是否启用了该工具
        if not self.is_tool_enabled:
            logger.warning(f"LLM尝试调用已禁用的 at_user 工具。调用者: {event.get_sender_name()}")
            return event.plain_result("抱歉，@用户工具当前不可用。")

        # 验证user_id是否为有效的QQ号（纯数字）
        if not user_id or not user_id.isdigit():
            logger.error(f"at_user工具调用失败：提供的user_id '{user_id}' 不是一个有效的数字ID。")
            return event.plain_result(f"工具调用失败：用户ID '{user_id}' 无效，必须是纯数字。")

        logger.info(f"LLM 正在调用 at_user 工具：@用户 {user_id}，消息：'{message}'")

        # 构建消息链 (MessageChain)
        message_chain = []

        # 1. 添加@组件
        message_chain.append(Comp.At(qq=int(user_id)))

        # 2. 添加前缀文本（如果配置了）和主要消息文本
        full_message = f" {self.at_prefix}{message}" if self.at_prefix else f" {message}"
        message_chain.append(Comp.Plain(text=full_message))

        # 3. 使用 chain_result 返回最终要发送给用户的完整消息链
        return event.chain_result(message_chain)

    async def terminate(self):
        """
        插件停用时调用的函数，用于释放资源。
        """
        logger.info("LLM @用户工具插件已卸载。")
        pass

