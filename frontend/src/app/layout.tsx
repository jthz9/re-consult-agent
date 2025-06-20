import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "재생에너지 AI 가이드",
  description: "정책/제도/RAG/예측/실시간 데이터 통합 상담 시스템",
  keywords: "재생에너지, 태양광, 풍력, AI, 챗봇, 정책, 제도",
  authors: [{ name: "재생에너지 AI 가이드 팀" }],
  viewport: "width=device-width, initial-scale=1",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body className={inter.className}>
        <div className="min-h-screen bg-gradient-to-br from-green-50 to-blue-50">
          {children}
        </div>
      </body>
    </html>
  );
}
