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
      setChatHistory((prev: ChatMessage[]) => [...prev, userMessage]);
      setIsLoading(true);
      setError(null);
      console.log("[Chatbot] 사용자 메시지 전송:", message);

      try {
        // 백엔드 API 호출
        const response = await api.chatWithBot(message);
        console.log("[Chatbot] API 응답:", response);

        // 실제 응답 구조에 맞게 content 파싱 (response.data?.response, response.response, response.message)
        const content =
          (response.data && (response.data as any).response) ??
          (response as any).response ??
          (response as any).message ??
          "죄송합니다. 일시적인 오류가 발생했습니다. 다시 시도해주세요.";

        if (
          response.status === "success" &&
          ((response.data && (response.data as any).response) ||
            (response as any).response ||
            (response as any).message)
        ) {
          const botMessage: ChatMessage = {
            type: "bot",
            content,
            timestamp: new Date().toISOString(),
          };
          setChatHistory((prev: ChatMessage[]) => [...prev, botMessage]);
        } else {
          // 에러 처리
          const errorMessage: ChatMessage = {
            type: "bot",
            content,
            timestamp: new Date().toISOString(),
          };
          setChatHistory((prev: ChatMessage[]) => [...prev, errorMessage]);
          setError(response.error || "알 수 없는 오류가 발생했습니다.");
          console.error("[Chatbot] API 오류:", response.error);
        }
      } catch (err) {
        console.error("[Chatbot] 네트워크/코드 에러:", err);
        const errorMessage: ChatMessage = {
          type: "bot",
          content: "서버 연결에 실패했습니다. 네트워크 상태를 확인해주세요.",
          timestamp: new Date().toISOString(),
        };
        setChatHistory((prev: ChatMessage[]) => [...prev, errorMessage]);
        setError(
          err instanceof Error ? err.message : "서버 연결에 실패했습니다."
        );
      } finally {
        setIsLoading(false);
        console.log("[Chatbot] 로딩 상태 종료");
      }
    },
    [isLoading]
  );

  const clearChat = useCallback(() => {
    setChatHistory([]);
    setError(null);
    console.log("[Chatbot] 대화 초기화");
  }, []);

  const getChatStats = useCallback(() => {
    const userMessages = chatHistory.filter(
      (msg: ChatMessage) => msg.type === "user"
    ).length;
    const botMessages = chatHistory.filter(
      (msg: ChatMessage) => msg.type === "bot"
    ).length;

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
