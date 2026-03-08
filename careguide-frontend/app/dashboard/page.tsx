export default function Dashboard() {
  return (
    <div className="font-display bg-background-light dark:bg-background-dark text-slate-900 dark:text-slate-100 min-h-screen relative">
      <div className="relative flex h-auto min-h-screen w-full flex-col group/design-root overflow-x-hidden">
        <div className="layout-container flex h-full grow flex-col">
          <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-slate-200 dark:border-slate-800 px-4 sm:px-6 md:px-10 py-3 md:py-4 bg-white dark:bg-[#15212d] sticky top-0 z-10 shadow-sm">
            <div className="flex items-center gap-2 sm:gap-4 text-primary">
              <span className="material-symbols-outlined text-2xl sm:text-3xl">ecg_heart</span>
              <h2 className="text-slate-900 dark:text-slate-100 text-lg sm:text-xl font-bold leading-tight tracking-[-0.015em]">CareGuide AI</h2>
            </div>
            <div className="flex flex-1 justify-end gap-4 sm:gap-8">
              <nav className="hidden md:flex items-center gap-8">
                <a className="text-primary text-sm font-semibold leading-normal border-b-2 border-primary pb-1" href="#">Dashboard</a>
                <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 text-sm font-medium leading-normal transition-colors" href="#">Prescriptions</a>
                <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 text-sm font-medium leading-normal transition-colors" href="#">Appointments</a>
                <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 text-sm font-medium leading-normal transition-colors" href="#">Billing</a>
                <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 text-sm font-medium leading-normal transition-colors" href="#">Settings</a>
              </nav>
              <div className="flex items-center gap-2 sm:gap-4">
                <button className="p-2 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors relative">
                  <span className="material-symbols-outlined">notifications</span>
                  <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
                </button>
                <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-8 sm:size-10 border-2 border-primary/20" data-alt="User profile picture" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuC6uYNQ2CbPIH6v7XE7hgSX7Ui0tcPVazby99AhHkwM5Ccuovm88u67nnCBnsRTt7tn8jRp5d5dU2TnCc1AjfzHlffc_YRuXEpd4fHusedeafad0Axx9k3Y_5W5fiwwr-AOqysrCJPsSN-eYkOnSLKGtP8Z4tuPLX8rYwKJ-JTWyA-l3R8NYX7Bmq7WYHGZc9wCk9tUiKJ_g0x3zBuvh9HX9cccVUZZ3ItymevJT3Blba5fKivp8BLXY7PXJZjON1SCAAj6Fqvyecxh")'}}></div>
                {/* Mobile Menu Button */}
                <button className="md:hidden p-2 text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-full transition-colors">
                  <span className="material-symbols-outlined">menu</span>
                </button>
              </div>
            </div>
          </header>
          <main className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-6 py-4 sm:py-6 md:py-8 flex flex-col gap-6 sm:gap-8">
            {/* Welcome Section */}
            <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
              <div className="flex flex-col gap-2">
                <h1 className="text-slate-900 dark:text-slate-100 text-2xl sm:text-3xl md:text-4xl font-black leading-tight tracking-[-0.033em]">Welcome back, John</h1>
                <p className="text-slate-500 dark:text-slate-400 text-sm sm:text-base font-normal leading-normal">Here is an overview of your health dashboard for today.</p>
              </div>
              <button className="bg-primary hover:bg-primary/90 text-white px-4 sm:px-6 py-2 sm:py-3 rounded-lg font-medium transition-colors shadow-md shadow-primary/20 flex items-center justify-center gap-2 text-sm sm:text-base min-h-[44px]">
                <span className="material-symbols-outlined text-lg sm:text-xl">add</span>
                Book Appointment
              </button>
            </div>
            {/* Quick Actions Grid */}
            <div>
              <h2 className="text-slate-900 dark:text-slate-100 text-lg sm:text-xl font-bold leading-tight tracking-[-0.015em] mb-3 sm:mb-4">Quick Actions</h2>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4 md:gap-6">
                <div className="bg-white dark:bg-[#15212d] p-4 sm:p-5 rounded-xl shadow-sm border border-slate-100 dark:border-slate-800 hover:shadow-md hover:border-primary/30 transition-all cursor-pointer group flex flex-col items-center text-center gap-3 sm:gap-4 min-h-[120px] sm:min-h-[140px]">
                  <div className="w-12 h-12 sm:w-16 sm:h-16 rounded-full bg-primary/10 text-primary flex items-center justify-center group-hover:scale-110 transition-transform">
                    <span className="material-symbols-outlined text-2xl sm:text-3xl">upload_file</span>
                  </div>
                  <div>
                    <h3 className="text-slate-900 dark:text-slate-100 text-sm sm:text-base font-semibold leading-normal">Upload Prescription</h3>
                    <p className="text-slate-500 dark:text-slate-400 text-xs sm:text-sm font-normal mt-1">Add new physical records</p>
                  </div>
                </div>
                <div className="bg-white dark:bg-[#15212d] p-4 sm:p-5 rounded-xl shadow-sm border border-slate-100 dark:border-slate-800 hover:shadow-md hover:border-primary/30 transition-all cursor-pointer group flex flex-col items-center text-center gap-3 sm:gap-4 min-h-[120px] sm:min-h-[140px]">
                  <div className="w-12 h-12 sm:w-16 sm:h-16 rounded-full bg-indigo-500/10 text-indigo-500 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <span className="material-symbols-outlined text-2xl sm:text-3xl">prescriptions</span>
                  </div>
                  <div>
                    <h3 className="text-slate-900 dark:text-slate-100 text-sm sm:text-base font-semibold leading-normal">Digital Prescriptions</h3>
                    <p className="text-slate-500 dark:text-slate-400 text-xs sm:text-sm font-normal mt-1">Access active medications</p>
                  </div>
                </div>
                <div className="bg-white dark:bg-[#15212d] p-4 sm:p-5 rounded-xl shadow-sm border border-slate-100 dark:border-slate-800 hover:shadow-md hover:border-primary/30 transition-all cursor-pointer group flex flex-col items-center text-center gap-3 sm:gap-4 min-h-[120px] sm:min-h-[140px]">
                  <div className="w-12 h-12 sm:w-16 sm:h-16 rounded-full bg-green-500/10 text-green-500 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <span className="material-symbols-outlined text-2xl sm:text-3xl">restaurant_menu</span>
                  </div>
                  <div>
                    <h3 className="text-slate-900 dark:text-slate-100 text-sm sm:text-base font-semibold leading-normal">Diet Plan</h3>
                    <p className="text-slate-500 dark:text-slate-400 text-xs sm:text-sm font-normal mt-1">View nutritional guidance</p>
                  </div>
                </div>
                <div className="bg-white dark:bg-[#15212d] p-4 sm:p-5 rounded-xl shadow-sm border border-slate-100 dark:border-slate-800 hover:shadow-md hover:border-primary/30 transition-all cursor-pointer group flex flex-col items-center text-center gap-3 sm:gap-4 min-h-[120px] sm:min-h-[140px]">
                  <div className="w-12 h-12 sm:w-16 sm:h-16 rounded-full bg-orange-500/10 text-orange-500 flex items-center justify-center group-hover:scale-110 transition-transform">
                    <span className="material-symbols-outlined text-2xl sm:text-3xl">fitness_center</span>
                  </div>
                  <div>
                    <h3 className="text-slate-900 dark:text-slate-100 text-sm sm:text-base font-semibold leading-normal">Exercise Plan</h3>
                    <p className="text-slate-500 dark:text-slate-400 text-xs sm:text-sm font-normal mt-1">Check daily workout routine</p>
                  </div>
                </div>
              </div>
            </div>
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 sm:gap-6 md:gap-8">
              {/* Upcoming Appointments */}
              <div className="lg:col-span-2 flex flex-col gap-4">
                <div className="flex items-center justify-between">
                  <h2 className="text-slate-900 dark:text-slate-100 text-lg sm:text-xl font-bold leading-tight tracking-[-0.015em]">Upcoming Appointments</h2>
                  <a className="text-primary text-sm font-medium hover:underline" href="#">View All</a>
                </div>
                <div className="flex flex-col gap-3 sm:gap-4">
                  {/* Appointment Card 1 */}
                  <div className="bg-white dark:bg-[#15212d] rounded-xl p-4 sm:p-5 shadow-sm border border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-start sm:items-center gap-4 sm:gap-5">
                    <div className="bg-primary/5 text-primary rounded-lg p-2 sm:p-3 text-center min-w-[70px] sm:min-w-[80px]">
                      <span className="block text-xs sm:text-sm font-semibold uppercase">Oct</span>
                      <span className="block text-xl sm:text-2xl font-bold">24</span>
                    </div>
                    <div className="flex-1 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 sm:gap-4 w-full">
                      <div className="flex gap-3 sm:gap-4 items-center">
                        <div className="w-10 h-10 sm:w-12 sm:h-12 rounded-full bg-slate-200 dark:bg-slate-700 bg-cover bg-center" data-alt="Doctor profile photo" style={{backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuAHZ_x1jx0ywTlivE2XWuLBUdsycI4DZBb_-nq-u9wq21ilCz9rvT0Rg8DsxHpCR0smSBmHS-2UKvCYSOP3hXOROr5K2cpNxjJxjSbuQFjIzeKsnt2yFC2gawbiYq2b7YBaTT0xiczWoNSakGgqjUEsESDzQPWqMvtgTj4gICNEEGSxXngp3j4Qfxo1-lyWQxEAZ2ddT2CHpaWnpp4fhsNj5aRYw7yGxD0wZHXy5ZghZ1tky3vHmnIcb4T5seQhlKxShSI4jefLr4ee')"}}></div>
                        <div>
                          <h4 className="text-slate-900 dark:text-slate-100 font-semibold text-sm sm:text-base">Dr. Sarah Jenkins</h4>
                          <p className="text-slate-500 dark:text-slate-400 text-xs sm:text-sm">Cardiologist • Video Consult</p>
                        </div>
                      </div>
                      <div className="flex flex-col sm:items-end gap-1 w-full sm:w-auto">
                        <div className="flex items-center gap-1 text-slate-700 dark:text-slate-300 text-xs sm:text-sm font-medium">
                          <span className="material-symbols-outlined text-sm sm:text-[18px]">schedule</span> 10:00 AM
                        </div>
                        <span className="px-2 py-1 bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400 rounded text-xs font-semibold self-start sm:self-end">Confirmed</span>
                      </div>
                    </div>
                  </div>
                  {/* Appointment Card 2 */}
                  <div className="bg-white dark:bg-[#15212d] rounded-xl p-5 shadow-sm border border-slate-100 dark:border-slate-800 flex flex-col sm:flex-row items-start sm:items-center gap-5">
                    <div className="bg-slate-50 dark:bg-slate-800 text-slate-600 dark:text-slate-400 rounded-lg p-3 text-center min-w-[80px]">
                      <span className="block text-sm font-semibold uppercase">Nov</span>
                      <span className="block text-2xl font-bold">02</span>
                    </div>
                    <div className="flex-1 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 w-full">
                      <div className="flex gap-4 items-center">
                        <div className="w-12 h-12 rounded-full bg-slate-200 dark:bg-slate-700 bg-cover bg-center" data-alt="Doctor profile photo" style={{backgroundImage: "url('https://lh3.googleusercontent.com/aida-public/AB6AXuBX6XlYAqbZbpJnEvqWxwvcsZd8EhXJw7n7d0oU9ebOCpJomRmPHndKj38TGWaMgnz_uazfHnrG6o6VfgCurzs-ZXyuz2SpQRX4LQlRm02161PY7kRfD_9JWiEsb2UaiTBAdzwzIOrA5w4mZQqjz_NHh5X3wZ2tB67Rhn9-PKvfRK5DeKh1VdqjfKxr7wvVPMlFKpgJHI0MxR4i8UmyJVpKruUkOvOmnHBv0w7qvmtTbY0-4KdM39ZZajUFrKOyvHyNv4xTNa7LlIs5')"}}></div>
                        <div>
                          <h4 className="text-slate-900 dark:text-slate-100 font-semibold">Dr. Michael Chen</h4>
                          <p className="text-slate-500 dark:text-slate-400 text-sm">General Practice • Clinic Visit</p>
                        </div>
                      </div>
                      <div className="flex flex-col sm:items-end gap-1">
                        <div className="flex items-center gap-1 text-slate-700 dark:text-slate-300 text-sm font-medium">
                          <span className="material-symbols-outlined text-[18px]">schedule</span> 2:30 PM
                        </div>
                        <span className="px-2.5 py-1 bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400 rounded text-xs font-semibold">Pending</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              {/* Recent Bills & Activity */}
              <div className="flex flex-col gap-4">
                <div className="flex items-center justify-between">
                  <h2 className="text-slate-900 dark:text-slate-100 text-xl font-bold leading-tight tracking-[-0.015em]">Recent Bills</h2>
                  <a className="text-primary text-sm font-medium hover:underline" href="#">History</a>
                </div>
                <div className="bg-white dark:bg-[#15212d] rounded-xl shadow-sm border border-slate-100 dark:border-slate-800 overflow-hidden">
                  <div className="p-4 border-b border-slate-100 dark:border-slate-800 flex justify-between items-center hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors cursor-pointer">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded bg-red-500/10 text-red-500 flex items-center justify-center">
                        <span className="material-symbols-outlined">receipt_long</span>
                      </div>
                      <div>
                        <h4 className="text-slate-900 dark:text-slate-100 font-medium text-sm">Lab Test - Blood Work</h4>
                        <p className="text-slate-500 dark:text-slate-400 text-xs mt-0.5">Oct 15, 2023</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="block text-slate-900 dark:text-slate-100 font-semibold">$125.00</span>
                      <span className="text-xs text-red-500 font-medium">Unpaid</span>
                    </div>
                  </div>
                  <div className="p-4 border-b border-slate-100 dark:border-slate-800 flex justify-between items-center hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors cursor-pointer">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 rounded bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 flex items-center justify-center">
                        <span className="material-symbols-outlined">receipt_long</span>
                      </div>
                      <div>
                        <h4 className="text-slate-900 dark:text-slate-100 font-medium text-sm">Consultation Fee</h4>
                        <p className="text-slate-500 dark:text-slate-400 text-xs mt-0.5">Sep 28, 2023</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <span className="block text-slate-900 dark:text-slate-100 font-semibold">$85.00</span>
                      <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">Paid</span>
                    </div>
                  </div>
                  <div className="p-4 bg-slate-50 dark:bg-slate-800/30 flex justify-between items-center">
                    <span className="text-sm text-slate-600 dark:text-slate-400 font-medium">Total Due</span>
                    <span className="text-lg text-slate-900 dark:text-slate-100 font-bold">$125.00</span>
                  </div>
                  <div className="p-4 pt-0 bg-slate-50 dark:bg-slate-800/30">
                    <button className="w-full bg-slate-900 dark:bg-slate-100 text-white dark:text-slate-900 py-2.5 rounded-lg text-sm font-semibold hover:bg-slate-800 dark:hover:bg-white transition-colors">Pay Now</button>
                  </div>
                </div>
              </div>
            </div>
          </main>
        </div>
      </div>
      {/* Floating Voice Assistant */}
      <button className="fixed bottom-8 right-8 w-16 h-16 bg-primary text-white rounded-full shadow-lg shadow-primary/40 flex items-center justify-center hover:scale-105 hover:bg-primary/90 transition-all z-50 group">
        <span className="material-symbols-outlined text-3xl group-hover:animate-pulse">mic</span>
      </button>
    </div>
  );
}