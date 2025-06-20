"use client";

export default function PolicyContent() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">정책/제도</h2>
        <p className="text-gray-600">재생에너지 관련 정책 및 제도 정보</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">정책 정보</h3>
        <div className="space-y-4">
          <div className="p-4 border rounded-lg">
            <h4 className="font-medium text-gray-900">재생에너지 3020 정책</h4>
            <p className="text-sm text-gray-600 mt-1">
              2030년까지 재생에너지 비중 20% 달성
            </p>
          </div>
          <div className="p-4 border rounded-lg">
            <h4 className="font-medium text-gray-900">태양광 발전 지원 제도</h4>
            <p className="text-sm text-gray-600 mt-1">
              태양광 발전소 설치 및 운영 지원
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
