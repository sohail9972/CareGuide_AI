export default function DietPlan() {
  return (
    <div className="relative flex h-auto min-h-screen w-full flex-col group/design-root overflow-x-hidden">
      <div className="layout-container flex h-full grow flex-col">
        <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-4 sm:px-6 md:px-10 py-3">
          <div className="flex items-center gap-2 sm:gap-4 text-slate-900 dark:text-slate-100">
            <div className="size-5 sm:size-6 text-primary">
              <svg className="w-full h-full" fill="none" viewBox="0 0 48 48" xmlns="http://www.w3.org/2000/svg">
                <path d="M44 11.2727C44 14.0109 39.8386 16.3957 33.69 17.6364C39.8386 18.877 44 21.2618 44 24C44 26.7382 39.8386 29.123 33.69 30.3636C39.8386 31.6043 44 33.9891 44 36.7273C44 40.7439 35.0457 44 24 44C12.9543 44 4 40.7439 4 36.7273C4 33.9891 8.16144 31.6043 14.31 30.3636C8.16144 29.123 4 26.7382 4 24C4 21.2618 8.16144 18.877 14.31 17.6364C8.16144 16.3957 4 14.0109 4 11.2727C4 7.25611 12.9543 4 24 4C35.0457 4 44 7.25611 44 11.2727Z" fill="currentColor"></path>
              </svg>
            </div>
            <h2 className="text-base sm:text-lg font-bold leading-tight tracking-[-0.015em]">CareGuide AI</h2>
          </div>
          <div className="flex flex-1 justify-end gap-4 sm:gap-8">
            <div className="flex items-center gap-4 sm:gap-9 hidden md:flex">
              <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 text-sm font-medium leading-normal" href="#">Dashboard</a>
              <a className="text-primary text-sm font-medium leading-normal" href="#">Diet Plan</a>
              <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 text-sm font-medium leading-normal" href="#">My Health</a>
              <a className="text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-100 text-sm font-medium leading-normal" href="#">Consultations</a>
            </div>
            <div className="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-8 sm:size-10 border border-slate-200 dark:border-slate-700" data-alt="User profile picture" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAijQ1hhBsFWHq_9Tkteoq_Iq8yoR-yagD8B0sFGAGqwUTpM-j9U4smTFlLDPf5pqWSISnRlvrFvueRMCxYAjFVz_TQl8NbZr78IzaR8hBvUQhxjuaHRHgCWibJ1IdJ03tx0_PPhpFtlkVeZtiagvBpUJUFoKBuQ-btZT73IqilGqR-JcWcNAD6Pc5FYCDyyepV27MBkBypGPhmOBBdZc3pnOYYy4sM03aA3EpGqozoxHPPkhObTO7w5wrphpXRTpLGEtQRYLr3SBEF")'}}></div>
          </div>
        </header>
        <div className="px-4 md:px-10 lg:px-40 flex flex-1 justify-center py-4 sm:py-5">
          <div className="layout-content-container flex flex-col max-w-[960px] flex-1">
            <div className="flex flex-wrap justify-between gap-3 p-3 sm:p-4">
              <div className="flex flex-col gap-3">
                <h1 className="text-2xl sm:text-3xl md:text-4xl font-black leading-tight tracking-[-0.033em]">AI-Driven Diet Plan</h1>
                <p className="text-slate-600 dark:text-slate-400 text-sm sm:text-base font-normal leading-normal">Personalized meals to accelerate your health recovery.</p>
              </div>
            </div>
            <div className="flex flex-col gap-3 p-3 sm:p-4 mt-2">
              <div className="flex gap-4 sm:gap-6 justify-between">
                <p className="text-sm sm:text-base font-medium leading-normal">Recovery Speed Indicator</p>
                <p className="text-sm font-bold text-green-600 dark:text-green-400">85%</p>
              </div>
              <div className="rounded-full bg-slate-200 dark:bg-slate-700 h-3 overflow-hidden">
                <div className="h-full rounded-full bg-gradient-to-r from-green-400 to-green-600" style={{width: '85%'}}></div>
              </div>
              <p className="text-slate-600 dark:text-slate-400 text-xs sm:text-sm font-normal leading-normal">Your current diet perfectly aligns with your recovery goals.</p>
            </div>
            <div className="flex items-center gap-3 sm:gap-4 bg-white dark:bg-slate-800 rounded-xl px-3 sm:px-4 py-3 min-h-14 justify-between mt-4 shadow-sm border border-slate-100 dark:border-slate-700 mx-3 sm:mx-4">
              <div className="flex items-center gap-3 sm:gap-4">
                <div className="text-primary flex items-center justify-center rounded-lg bg-primary/10 shrink-0 size-9 sm:size-10">
                  <span className="material-symbols-outlined text-lg sm:text-xl">sell</span>
                </div>
                <div className="flex flex-col">
                  <p className="text-sm sm:text-base font-medium leading-normal flex-1 truncate">Affordable Options</p>
                  <p className="text-xs text-slate-500 dark:text-slate-400">Prioritize budget-friendly ingredients</p>
                </div>
              </div>
              <div className="shrink-0">
                <label className="relative flex h-7 w-12 cursor-pointer items-center rounded-full border-none bg-slate-200 dark:bg-slate-600 p-0.5 has-[:checked]:justify-end has-[:checked]:bg-primary transition-colors duration-200">
                  <div className="h-6 w-6 rounded-full bg-white shadow-sm transition-transform duration-200"></div>
                  <input checked className="invisible absolute" type="checkbox"/>
                </label>
              </div>
            </div>
            <div className="mt-8 pb-3 overflow-x-auto">
              <div className="flex border-b border-slate-200 dark:border-slate-800 px-4 gap-8 min-w-max">
                <a className="flex flex-col items-center justify-center border-b-[3px] border-b-primary text-primary pb-3 pt-4 px-2" href="#">
                  <p className="text-sm font-bold leading-normal tracking-[0.015em]">Today</p>
                </a>
                <a className="flex flex-col items-center justify-center border-b-[3px] border-b-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 pb-3 pt-4 px-2" href="#">
                  <p className="text-sm font-semibold leading-normal tracking-[0.015em]">Tomorrow</p>
                </a>
                <a className="flex flex-col items-center justify-center border-b-[3px] border-b-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 pb-3 pt-4 px-2" href="#">
                  <p className="text-sm font-semibold leading-normal tracking-[0.015em]">Wednesday</p>
                </a>
                <a className="flex flex-col items-center justify-center border-b-[3px] border-b-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 pb-3 pt-4 px-2" href="#">
                  <p className="text-sm font-semibold leading-normal tracking-[0.015em]">Thursday</p>
                </a>
                <a className="flex flex-col items-center justify-center border-b-[3px] border-b-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 pb-3 pt-4 px-2" href="#">
                  <p className="text-sm font-semibold leading-normal tracking-[0.015em]">Friday</p>
                </a>
                <a className="flex flex-col items-center justify-center border-b-[3px] border-b-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 pb-3 pt-4 px-2" href="#">
                  <p className="text-sm font-semibold leading-normal tracking-[0.015em]">Saturday</p>
                </a>
                <a className="flex flex-col items-center justify-center border-b-[3px] border-b-transparent text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200 pb-3 pt-4 px-2" href="#">
                  <p className="text-sm font-semibold leading-normal tracking-[0.015em]">Sunday</p>
                </a>
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6 p-4 mt-4">
              <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 overflow-hidden flex flex-col">
                <div className="h-32 sm:h-40 bg-cover bg-center" data-alt="Oatmeal with berries" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAtRqcpLYvfklIPj1OwApY7fQISI5LzFoWzjK6vNEfhoFHQzpHNukbZ9CTMiiEbGsVXFr8sW6W45T0SNSvCsehiIpMTmde_I8MzXWSlfMsJsR2Ue1GzW5v7e2hPb8652bqudiVj0U1CfGYFW4d_0p0Omfzc193kUOyMvrTbFIWEg-ziCmCXhQJirPsWK4qxgnFjD7HPyyzOGb1-3CtOyCx_naeg_nBMtIkp6s2zsS1gZHLFfGmO2gSHIDa4S3xVbgewHFxGP9RncaA1")'}}></div>
                <div className="p-4 sm:p-5 flex flex-col flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="material-symbols-outlined text-orange-400 text-lg sm:text-xl">wb_twilight</span>
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Breakfast</span>
                  </div>
                  <h3 className="text-base sm:text-lg font-bold mb-1">Antioxidant Berry Oatmeal</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-4 flex-1">Rich in fiber and antioxidants to reduce inflammation and provide sustained energy.</p>
                  <div className="flex items-center justify-between mt-auto pt-4 border-t border-slate-100 dark:border-slate-700">
                    <div className="flex items-center gap-1 text-xs font-medium text-slate-500 dark:text-slate-400">
                      <span className="material-symbols-outlined text-base">local_fire_department</span>
                      320 kcal
                    </div>
                    <button className="text-primary text-sm font-semibold hover:underline min-h-[44px] flex items-center">Swap Meal</button>
                  </div>
                </div>
              </div>
              <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 overflow-hidden flex flex-col">
                <div className="h-32 sm:h-40 bg-cover bg-center" data-alt="Healthy salad bowl" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAecEcqnDz5tEk_anTyfvkLaKDjsW-YFtS0fkWHPf8Ihw7WorVt-clGH8RaDJZ5KBAsHLnPtajywVYhfw_LLXDLeeXpf8QuhHJAT2sLf7aMVWldRAItLz7UUt6g2TvpftuTBOhd7sGc-1oFlSRN051WG2Qz4iVr8Kuuj1R9tKTKOsnXEcc3XaSLkU5hAhh5o4Ykmt7UStotO_nOY90hivaG_wwCPmCk2NeWv5T-MalCkEDSORN0pHX1Hw7hk6VHGH4Dg__AzjNWCE4D")'}}></div>
                <div className="p-4 sm:p-5 flex flex-col flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="material-symbols-outlined text-yellow-500 text-lg sm:text-xl">light_mode</span>
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Lunch</span>
                  </div>
                  <h3 className="text-base sm:text-lg font-bold mb-1">Quinoa Super Salad</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-4 flex-1">Packed with plant-based protein and essential vitamins for cellular repair.</p>
                  <div className="flex items-center justify-between mt-auto pt-4 border-t border-slate-100 dark:border-slate-700">
                    <div className="flex items-center gap-1 text-xs font-medium text-slate-500 dark:text-slate-400">
                      <span className="material-symbols-outlined text-base">local_fire_department</span>
                      450 kcal
                    </div>
                    <button className="text-primary text-sm font-semibold hover:underline min-h-[44px] flex items-center">Swap Meal</button>
                  </div>
                </div>
              </div>
              <div className="bg-white dark:bg-slate-800 rounded-2xl shadow-sm border border-slate-100 dark:border-slate-700 overflow-hidden flex flex-col">
                <div className="h-32 sm:h-40 bg-cover bg-center" data-alt="Grilled salmon with vegetables" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuCvkOCDEfM6RDqz9jgntTpScrWOyC1zMe6YfPX6yWO0OQhNIgiZcS6QAJBRV7_b-8QTJo4Grd9VgiQLrJKkSALXOWU_zh1X6ZYYvhkUuTvUkKb-LAEhY_TdUr0ZCyqSx4MzeIBQn0lV4Ix5yxynlXmUVR9S8PObN8xnnUJH1OhE_QZtwdjxti8PIguMb8muDJpOx3V0YQoCHkTDDyEvPTGshO-B4bGDTjLKV5UFEdF3cm66RL7SS4KJ3_GyPx8SaO6S_J04Au3ndluM")'}}></div>
                <div className="p-4 sm:p-5 flex flex-col flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="material-symbols-outlined text-indigo-400 text-lg sm:text-xl">dark_mode</span>
                    <span className="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">Dinner</span>
                  </div>
                  <h3 className="text-base sm:text-lg font-bold mb-1">Omega-3 Grilled Salmon</h3>
                  <p className="text-sm text-slate-600 dark:text-slate-400 mb-4 flex-1">High in healthy fats crucial for joint health and cognitive function recovery.</p>
                  <div className="flex items-center justify-between mt-auto pt-4 border-t border-slate-100 dark:border-slate-700">
                    <div className="flex items-center gap-1 text-xs font-medium text-slate-500 dark:text-slate-400">
                      <span className="material-symbols-outlined text-base">local_fire_department</span>
                      520 kcal
                    </div>
                    <button className="text-primary text-sm font-semibold hover:underline min-h-[44px] flex items-center">Swap Meal</button>
                  </div>
                </div>
              </div>
            </div>
            <div className="p-4 mt-4 flex justify-center">
              <button className="bg-primary hover:bg-primary/90 text-white font-semibold py-3 px-8 rounded-full shadow-sm transition-colors flex items-center gap-2 min-h-[44px]">
                <span className="material-symbols-outlined text-xl">grocery</span>
                Generate Shopping List
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}