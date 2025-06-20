import { useState, useEffect } from "react";
import { api } from "@/services/api";

export interface SystemStatus {
  fastapi: "healthy" | "error" | "checking";
  chroma: "healthy" | "error" | "checking";
  ml: "healthy" | "error" | "checking";
}

export interface SystemInfo {
  embedding_model: string;
  vectorstore_path: string;
  collection_name: string;
}

export function useSystemStatus() {
  const [systemStatus, setSystemStatus] = useState<SystemStatus>({
    fastapi: "checking",
    chroma: "checking",
    ml: "checking",
  });
  const [systemInfo, setSystemInfo] = useState<SystemInfo | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const checkSystemStatus = async () => {
    try {
      setIsLoading(true);
      setError(null);

      // 헬스 체크
      const healthResponse = await api.healthCheck();
      const chatbotResponse = await api.getChatbotStatus();
      const systemInfoResponse = await api.getSystemInfo();

      setSystemStatus({
        fastapi: healthResponse.status === "success" ? "healthy" : "error",
        chroma: healthResponse.status === "success" ? "healthy" : "error",
        ml: chatbotResponse.status === "success" ? "healthy" : "error",
      });

      if (systemInfoResponse.status === "success" && systemInfoResponse.data) {
        setSystemInfo(systemInfoResponse.data.system_info);
      }
    } catch (err) {
      console.error("System status check failed:", err);
      setError(
        err instanceof Error ? err.message : "시스템 상태 확인에 실패했습니다."
      );
      setSystemStatus({
        fastapi: "error",
        chroma: "error",
        ml: "error",
      });
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    checkSystemStatus();

    // 30초마다 시스템 상태 재확인
    const interval = setInterval(checkSystemStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  return {
    systemStatus,
    systemInfo,
    isLoading,
    error,
    refresh: checkSystemStatus,
  };
}
