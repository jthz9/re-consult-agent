"use client";

export default function MLPredictionContent() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">ML 예측</h2>
        <p className="text-gray-600">머신러닝 기반 발전량 예측</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">예측 결과</h3>
        <div className="h-64 bg-gray-100 rounded-lg flex items-center justify-center">
          <p className="text-gray-500">ML 예측 결과가 여기에 표시됩니다</p>
        </div>
      </div>
    </div>
  );
}
