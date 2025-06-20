"use client";

import {
  Sun,
  Wind,
  MessageSquare,
  BarChart3,
  TrendingUp,
  Zap,
  Settings,
  Users,
} from "lucide-react";

interface SidebarProps {
  activeTab: string;
  onTabChange: (tab: string) => void;
}

export default function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  const menuItems = [
    { id: "dashboard", label: "대시보드", icon: BarChart3 },
    { id: "chatbot", label: "AI 챗봇", icon: MessageSquare },
    { id: "visualization", label: "발전량 시각화", icon: TrendingUp },
    { id: "ml-prediction", label: "ML 예측", icon: Zap },
    { id: "policy", label: "정책/제도", icon: Settings },
    { id: "users", label: "사용자 관리", icon: Users },
  ];

  return (
    <div className="w-64 bg-white shadow-lg">
      <div className="p-6">
        <div className="flex items-center space-x-3">
          <div className="flex space-x-1">
            <Sun className="h-6 w-6 text-yellow-500" />
            <Wind className="h-6 w-6 text-blue-500" />
          </div>
          <h1 className="text-xl font-bold text-gray-800">
            재생에너지 AI 가이드
          </h1>
        </div>
      </div>

      <nav className="mt-6">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => onTabChange(item.id)}
              className={`w-full flex items-center space-x-3 px-6 py-3 text-left transition-colors ${
                activeTab === item.id
                  ? "bg-green-50 border-r-2 border-green-500 text-green-700"
                  : "text-gray-600 hover:bg-gray-50"
              }`}
            >
              <Icon className="h-5 w-5" />
              <span className="font-medium">{item.label}</span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}
