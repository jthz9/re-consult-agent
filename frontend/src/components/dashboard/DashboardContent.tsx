"use client";

import {
  Sun,
  Wind,
  MessageSquare,
  Zap,
  Loader2,
  RefreshCw,
} from "lucide-react";
import { useSystemStatus } from "@/hooks/useSystemStatus";

export default function DashboardContent() {
  const { systemStatus, systemInfo, isLoading, error, refresh } =
    useSystemStatus();

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "healthy":
        return (
          <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">
            정상
          </span>
        );
      case "error":
        return (
          <span className="px-2 py-1 text-xs bg-red-100 text-red-800 rounded-full">
            오류
          </span>
        );
      case "checking":
        return (
          <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded-full flex items-center space-x-1">
            <Loader2 className="h-3 w-3 animate-spin" />
            <span>확인 중</span>
          </span>
        );
      default:
        return (
          <span className="px-2 py-1 text-xs bg-gray-100 text-gray-800 rounded-full">
            알 수 없음
          </span>
        );
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">대시보드</h2>
          <p className="text-gray-600">재생에너지 AI 가이드 시스템 현황</p>
        </div>
        <button
          onClick={refresh}
          disabled={isLoading}
          className="flex items-center space-x-2 px-3 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors disabled:bg-gray-300 disabled:cursor-not-allowed"
        >
          <RefreshCw className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} />
          <span>새로고침</span>
        </button>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800 text-sm">{error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-green-100 rounded-lg">
              <Sun className="h-6 w-6 text-green-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">태양광 발전량</p>
              <p className="text-2xl font-bold text-gray-900">2,847 MW</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-blue-100 rounded-lg">
              <Wind className="h-6 w-6 text-blue-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">풍력 발전량</p>
              <p className="text-2xl font-bold text-gray-900">1,234 MW</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-purple-100 rounded-lg">
              <MessageSquare className="h-6 w-6 text-purple-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">챗봇 대화</p>
              <p className="text-2xl font-bold text-gray-900">156회</p>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <div className="flex items-center">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Zap className="h-6 w-6 text-orange-600" />
            </div>
            <div className="ml-4">
              <p className="text-sm font-medium text-gray-600">ML 예측</p>
              <p className="text-2xl font-bold text-gray-900">89%</p>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            최근 활동
          </h3>
          <div className="space-y-3">
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-gray-600">
                태양광 발전소 데이터 업데이트
              </span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
              <span className="text-sm text-gray-600">ML 모델 재학습 완료</span>
            </div>
            <div className="flex items-center space-x-3">
              <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
              <span className="text-sm text-gray-600">
                새로운 정책 정보 추가
              </span>
            </div>
          </div>
        </div>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">
            시스템 상태
          </h3>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">FastAPI 서버</span>
              {getStatusBadge(systemStatus.fastapi)}
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">Chroma DB</span>
              {getStatusBadge(systemStatus.chroma)}
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-600">ML 모델</span>
              {getStatusBadge(systemStatus.ml)}
            </div>
            {systemInfo && (
              <div className="mt-4 pt-4 border-t">
                <h4 className="text-sm font-medium text-gray-900 mb-2">
                  시스템 정보
                </h4>
                <div className="space-y-1 text-xs text-gray-600">
                  <p>임베딩 모델: {systemInfo.embedding_model}</p>
                  <p>벡터스토어: {systemInfo.collection_name}</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
