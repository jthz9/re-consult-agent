"use client";

export default function UsersContent() {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-2">사용자 관리</h2>
        <p className="text-gray-600">시스템 사용자 관리 및 권한 설정</p>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-sm border">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">
          사용자 목록
        </h3>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div>
              <h4 className="font-medium text-gray-900">관리자</h4>
              <p className="text-sm text-gray-600">admin@example.com</p>
            </div>
            <span className="px-2 py-1 text-xs bg-red-100 text-red-800 rounded-full">
              관리자
            </span>
          </div>
          <div className="flex items-center justify-between p-4 border rounded-lg">
            <div>
              <h4 className="font-medium text-gray-900">일반 사용자</h4>
              <p className="text-sm text-gray-600">user@example.com</p>
            </div>
            <span className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
              사용자
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
