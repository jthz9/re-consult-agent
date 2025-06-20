import { useState, useCallback } from "react";
import { api, ChatMessage } from "@/services/api";

export function useChatbot() {
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (message: string) => {
      if (!message.trim() || isLoading) return;

      const userMessage: ChatMessage = {
        type: "user",
        content: message,
        timestamp: new Date().toISOString(),
      };

      // 사용자 메시지 추가
      setChatHistory((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setError(null);

      try {
        // 백엔드 API 호출
        const response = await api.chatWithBot(message);

        if (response.status === "success" && response.data) {
          const botMessage: ChatMessage = {
            type: "bot",
            content: response.data.response,
            timestamp: new Date().toISOString(),
          };
          setChatHistory((prev) => [...prev, botMessage]);
        } else {
          // 에러 처리
          const errorMessage: ChatMessage = {
            type: "bot",
            content:
              "죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요.",
            timestamp: new Date().toISOString(),
          };
          setChatHistory((prev) => [...prev, errorMessage]);
          setError(response.error || "알 수 없는 오류가 발생했습니다.");
        }
      } catch (err) {
        console.error("Chat API error:", err);
        const errorMessage: ChatMessage = {
          type: "bot",
          content: "서버 연결에 실패했습니다. 네트워크 상태를 확인해주세요.",
          timestamp: new Date().toISOString(),
        };
        setChatHistory((prev) => [...prev, errorMessage]);
        setError(
          err instanceof Error ? err.message : "서버 연결에 실패했습니다."
        );
      } finally {
        setIsLoading(false);
      }
    },
    [isLoading]
  );

  const clearChat = useCallback(() => {
    setChatHistory([]);
    setError(null);
  }, []);

  const getChatStats = useCallback(() => {
    const userMessages = chatHistory.filter(
      (msg) => msg.type === "user"
    ).length;
    const botMessages = chatHistory.filter((msg) => msg.type === "bot").length;

    return {
      totalMessages: chatHistory.length,
      userMessages,
      botMessages,
      hasError: error !== null,
    };
  }, [chatHistory, error]);

  return {
    chatHistory,
    isLoading,
    error,
    sendMessage,
    clearChat,
    getChatStats,
  };
}
