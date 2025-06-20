"use client";

export default function VisualizationContent() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">발전량 시각화</h2>
        <p className="text-gray-600">실시간 발전량 데이터 및 차트</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">차트 영역</h3>
        <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
          <p className="text-gray-500">
            Recharts를 사용한 발전량 차트가 여기에 표시됩니다
          </p>
        </div>
      </div>
    </div>
  );
}
