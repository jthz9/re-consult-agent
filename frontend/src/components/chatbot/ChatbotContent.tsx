"use client";

import { useState } from "react";
import { MessageSquare, Loader2, Trash2 } from "lucide-react";
import { useChatbot } from "@/hooks/useChatbot";

export default function ChatbotContent() {
  const [message, setMessage] = useState("");
  const {
    chatHistory,
    isLoading,
    error,
    sendMessage,
    clearChat,
    getChatStats,
  } = useChatbot();

  const handleSendMessage = async () => {
    if (!message.trim()) return;
    await sendMessage(message);
    setMessage("");
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const chatStats = getChatStats();

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">AI 챗봇</h2>
          <p className="text-gray-600">재생에너지 관련 질문에 답변드립니다</p>
        </div>
        <div className="flex items-center space-x-4">
          <div className="text-sm text-gray-600">
            총 {chatStats.totalMessages}개 메시지
          </div>
          <button
            onClick={clearChat}
            disabled={chatHistory.length === 0}
            className="flex items-center space-x-2 px-3 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
          >
            <Trash2 className="h-4 w-4" />
            <span>대화 초기화</span>
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800 text-sm">{error}</p>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-sm border h-96 flex flex-col">
        <div className="flex-1 p-4 overflow-y-auto space-y-4">
          {chatHistory.length === 0 ? (
            <div className="text-center text-gray-500 mt-20">
              <MessageSquare className="h-12 w-12 mx-auto mb-4 text-gray-300" />
              <p>재생에너지 관련 질문을 입력해주세요</p>
            </div>
          ) : (
            chatHistory.map((chat, index) => (
              <div
                key={index}
                className={`flex ${
                  chat.type === "user" ? "justify-end" : "justify-start"
                }`}
              >
                <div
                  className={`max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                    chat.type === "user"
                      ? "bg-green-500 text-white"
                      : "bg-gray-100 text-gray-800"
                  }`}
                >
                  {chat.content}
                </div>
              </div>
            ))
          )}
          {isLoading && (
            <div className="flex justify-start">
              <div className="bg-gray-100 text-gray-800 px-4 py-2 rounded-lg flex items-center space-x-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>답변을 생성하고 있습니다...</span>
              </div>
            </div>
          )}
        </div>

        <div className="border-t p-4">
          <div className="flex space-x-2">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="질문을 입력하세요..."
              disabled={isLoading}
              className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-green-500 disabled:bg-gray-50 disabled:text-gray-500"
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading || !message.trim()}
              className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              {isLoading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>전송 중...</span>
                </>
              ) : (
                <span>전송</span>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
