// API 기본 설정
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// API 응답 타입 정의
export interface ApiResponse<T = unknown> {
  status: "success" | "error";
  data?: T;
  error?: string;
  message?: string;
}

// 챗봇 응답 타입
export interface ChatMessage {
  type: "user" | "bot";
  content: string;
  timestamp?: string;
}

export interface ChatResponse {
  status: "success" | "error";
  message: string;
  response: string;
}

// 시스템 정보 타입
export interface SystemInfo {
  embedding_model: string;
  vectorstore_path: string;
  collection_name: string;
}

// RAG 검색 결과 타입
export interface RAGSearchResult {
  status: "success" | "error";
  query: string;
  result: Record<string, unknown>;
}

// API 클라이언트 클래스
class ApiClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  // 기본 HTTP 요청 메서드
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const url = `${this.baseURL}${endpoint}`;
      const response = await fetch(url, {
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
        ...options,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      return data;
    } catch (error) {
      console.error("API request failed:", error);
      return {
        status: "error",
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  // GET 요청
  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: "GET" });
  }

  // POST 요청
  async post<T>(
    endpoint: string,
    data?: Record<string, unknown>
  ): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: "POST",
      body: data ? JSON.stringify(data) : undefined,
    });
  }

  // 헬스 체크
  async healthCheck(): Promise<ApiResponse> {
    return this.get("/health");
  }

  // 챗봇과 대화
  async chatWithBot(message: string): Promise<ApiResponse<ChatResponse>> {
    return this.post<ChatResponse>("/api/chat", { message });
  }

  // 챗봇 상태 확인
  async getChatbotStatus(): Promise<ApiResponse> {
    return this.get("/api/chatbot/status");
  }

  // RAG 검색
  async ragSearch(
    query: string,
    k: number = 3
  ): Promise<ApiResponse<RAGSearchResult>> {
    return this.get<RAGSearchResult>(
      `/api/rag/search?query=${encodeURIComponent(query)}&k=${k}`
    );
  }

  // 시스템 정보
  async getSystemInfo(): Promise<ApiResponse<{ system_info: SystemInfo }>> {
    return this.get<{ system_info: SystemInfo }>("/api/system/info");
  }
}

// API 클라이언트 인스턴스 생성
export const apiClient = new ApiClient();

// 편의 함수들
export const api = {
  healthCheck: () => apiClient.healthCheck(),
  chatWithBot: (message: string) => apiClient.chatWithBot(message),
  getChatbotStatus: () => apiClient.getChatbotStatus(),
  ragSearch: (query: string, k?: number) => apiClient.ragSearch(query, k),
  getSystemInfo: () => apiClient.getSystemInfo(),
};
