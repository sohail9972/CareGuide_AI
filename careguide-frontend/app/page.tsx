import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-background-light dark:bg-background-dark font-display">
      <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-slate-200 dark:border-slate-800 px-4 sm:px-6 md:px-10 py-4 bg-white dark:bg-slate-900">
        <div className="flex items-center gap-4 text-primary">
          <span className="material-symbols-outlined text-2xl sm:text-3xl">medical_services</span>
          <h2 className="text-slate-900 dark:text-slate-100 text-lg sm:text-xl font-bold leading-tight tracking-[-0.015em]">CareGuide AI</h2>
        </div>
      </header>
      <main className="container mx-auto px-4 sm:px-6 py-8 sm:py-12">
        <div className="text-center mb-8 sm:mb-12">
          <h1 className="text-2xl sm:text-3xl md:text-4xl font-black text-slate-900 dark:text-slate-100 mb-4">Welcome to CareGuide AI</h1>
          <p className="text-base sm:text-lg text-slate-600 dark:text-slate-400 max-w-2xl mx-auto px-4">
            AI-powered healthcare platform for personalized medical assistance, prescription management, and health tracking.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6 max-w-6xl mx-auto px-4">
          <Link href="/auth/login" className="bg-white dark:bg-slate-800 rounded-xl p-4 sm:p-6 shadow-sm border border-slate-100 dark:border-slate-700 hover:shadow-md transition-shadow min-h-[120px] sm:min-h-[140px]">
            <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-primary/10 text-primary flex items-center justify-center mb-4">
              <span className="material-symbols-outlined text-xl sm:text-2xl">login</span>
            </div>
            <h3 className="text-base sm:text-lg font-semibold text-slate-900 dark:text-slate-100 mb-2">Authentication</h3>
            <p className="text-slate-600 dark:text-slate-400 text-sm">Secure login for patients and doctors</p>
          </Link>
          <Link href="/dashboard" className="bg-white dark:bg-slate-800 rounded-xl p-4 sm:p-6 shadow-sm border border-slate-100 dark:border-slate-700 hover:shadow-md transition-shadow min-h-[120px] sm:min-h-[140px]">
            <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-green-500/10 text-green-500 flex items-center justify-center mb-4">
              <span className="material-symbols-outlined text-xl sm:text-2xl">dashboard</span>
            </div>
            <h3 className="text-base sm:text-lg font-semibold text-slate-900 dark:text-slate-100 mb-2">Patient Dashboard</h3>
            <p className="text-slate-600 dark:text-slate-400 text-sm">Overview of health metrics and appointments</p>
          </Link>
          <Link href="/diet-plan" className="bg-white dark:bg-slate-800 rounded-xl p-4 sm:p-6 shadow-sm border border-slate-100 dark:border-slate-700 hover:shadow-md transition-shadow min-h-[120px] sm:min-h-[140px]">
            <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-orange-500/10 text-orange-500 flex items-center justify-center mb-4">
              <span className="material-symbols-outlined text-xl sm:text-2xl">restaurant_menu</span>
            </div>
            <h3 className="text-base sm:text-lg font-semibold text-slate-900 dark:text-slate-100 mb-2">AI Diet Plan</h3>
            <p className="text-slate-600 dark:text-slate-400 text-sm">Personalized meal recommendations</p>
          </Link>
        </div>
        <div className="text-center mt-8 sm:mt-12 px-4">
          <p className="text-slate-500 dark:text-slate-400">
            More pages are being implemented. Check back soon for additional features.
          </p>
        </div>
      </main>
    </div>
  );
}
