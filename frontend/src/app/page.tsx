"use client";

import { useState } from "react";
import Sidebar from "@/components/layout/Sidebar";
import DashboardContent from "@/components/dashboard/DashboardContent";
import ChatbotContent from "@/components/chatbot/ChatbotContent";
import VisualizationContent from "@/components/visualization/VisualizationContent";
import MLPredictionContent from "@/components/ml/MLPredictionContent";
import PolicyContent from "@/components/policy/PolicyContent";
import UsersContent from "@/components/users/UsersContent";

export default function Home() {
  const [activeTab, setActiveTab] = useState("dashboard");

  const renderContent = () => {
    switch (activeTab) {
      case "dashboard":
        return <DashboardContent />;
      case "chatbot":
        return <ChatbotContent />;
      case "visualization":
        return <VisualizationContent />;
      case "ml-prediction":
        return <MLPredictionContent />;
      case "policy":
        return <PolicyContent />;
      case "users":
        return <UsersContent />;
      default:
        return <DashboardContent />;
    }
  };

  return (
    <div className="flex h-screen bg-gray-50">
      {/* 사이드바 */}
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />

      {/* 메인 콘텐츠 */}
      <div className="flex-1 overflow-auto">
        <div className="p-8">{renderContent()}</div>
      </div>
    </div>
  );
}
