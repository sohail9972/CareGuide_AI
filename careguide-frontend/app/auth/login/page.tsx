export default function Login() {
  return (
    <div className="bg-background-light dark:bg-background-dark font-display text-slate-900 dark:text-slate-100 min-h-screen flex flex-col">
      <header className="flex items-center justify-between whitespace-nowrap border-b border-solid border-slate-200 dark:border-slate-800 bg-white dark:bg-[#1a2530] px-4 sm:px-6 md:px-10 py-4 shadow-sm">
        <div className="flex items-center gap-4 text-primary">
          <span className="material-symbols-outlined text-2xl sm:text-3xl">medical_services</span>
          <h2 className="text-slate-900 dark:text-slate-100 text-lg sm:text-xl font-bold leading-tight tracking-[-0.015em]">CareGuide AI</h2>
        </div>
        <div className="flex flex-1 justify-end gap-8">
          <div className="flex items-center gap-4 sm:gap-9 hidden md:flex">
            <a className="text-slate-600 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium leading-normal" href="#">Help Center</a>
            <a className="text-slate-600 dark:text-slate-300 hover:text-primary dark:hover:text-primary transition-colors text-sm font-medium leading-normal" href="#">Contact Support</a>
            <div className="flex items-center gap-2 text-primary bg-primary/10 px-3 py-1.5 rounded-full cursor-pointer hover:bg-primary/20 transition-colors">
              <span className="material-symbols-outlined text-sm">mic</span>
              <span className="text-sm font-medium">Voice Setup</span>
            </div>
          </div>
        </div>
      </header>
      <main className="flex-1 flex items-center justify-center p-4 sm:p-6">
        <div className="w-full max-w-md bg-white dark:bg-[#1a2530] rounded-xl shadow-lg border border-slate-100 dark:border-slate-800 overflow-hidden">
          <div className="p-6 sm:p-8 text-center border-b border-slate-100 dark:border-slate-800">
            <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 dark:text-slate-100 mb-2">Welcome Back</h1>
            <p className="text-slate-500 dark:text-slate-400 text-sm">Secure and accessible healthcare assistance.</p>
          </div>
          <div className="p-6 sm:p-8 space-y-6">
            {/* Role Toggle */}
            <div className="flex h-12 flex-1 items-center justify-center rounded-lg bg-slate-100 dark:bg-slate-800 p-1">
              <label className="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-md px-2 has-[:checked]:bg-white dark:has-[:checked]:bg-[#2a3644] has-[:checked]:shadow-sm has-[:checked]:text-primary dark:has-[:checked]:text-primary text-slate-500 dark:text-slate-400 text-sm font-semibold transition-all">
                <span className="material-symbols-outlined text-sm mr-2">person</span>
                <span className="truncate">Patient</span>
                <input checked className="invisible w-0" name="role_select" type="radio" value="Patient"/>
              </label>
              <label className="flex cursor-pointer h-full grow items-center justify-center overflow-hidden rounded-md px-2 has-[:checked]:bg-white dark:has-[:checked]:bg-[#2a3644] has-[:checked]:shadow-sm has-[:checked]:text-primary dark:has-[:checked]:text-primary text-slate-500 dark:text-slate-400 text-sm font-semibold transition-all">
                <span className="material-symbols-outlined text-sm mr-2">stethoscope</span>
                <span className="truncate">Doctor</span>
                <input className="invisible w-0" name="role_select" type="radio" value="Doctor"/>
              </label>
            </div>
            {/* Form Fields */}
            <div className="space-y-4">
              <label className="flex flex-col flex-1">
                <span className="text-slate-700 dark:text-slate-300 text-sm font-medium pb-2">Email Address</span>
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">mail</span>
                  <input className="form-input flex w-full flex-1 rounded-lg text-slate-900 dark:text-slate-100 bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 focus:border-primary dark:focus:border-primary focus:ring-1 focus:ring-primary h-12 pl-12 pr-4 text-base placeholder:text-slate-400 transition-colors" placeholder="Enter your email" type="email"/>
                </div>
              </label>
              <label className="flex flex-col flex-1">
                <div className="flex justify-between pb-2">
                  <span className="text-slate-700 dark:text-slate-300 text-sm font-medium">Password</span>
                  <a className="text-sm text-primary hover:underline font-medium" href="#">Forgot?</a>
                </div>
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">lock</span>
                  <input className="form-input flex w-full flex-1 rounded-lg text-slate-900 dark:text-slate-100 bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 focus:border-primary dark:focus:border-primary focus:ring-1 focus:ring-primary h-12 pl-12 pr-4 text-base placeholder:text-slate-400 transition-colors" placeholder="Enter your password" type="password"/>
                  <button className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200" type="button">
                    <span className="material-symbols-outlined">visibility_off</span>
                  </button>
                </div>
              </label>
            </div>
            {/* Actions */}
            <div className="pt-2">
              <button className="w-full flex cursor-pointer items-center justify-center rounded-lg h-12 px-4 bg-primary hover:bg-primary/90 text-white text-base font-bold transition-colors shadow-md shadow-primary/20 min-h-[44px]">
                Log In
              </button>
            </div>
            <div className="text-center pt-4">
              <p className="text-slate-500 dark:text-slate-400 text-sm">
                Don&apos;t have an account? <a className="text-primary font-semibold hover:underline" href="#">Sign up</a>
              </p>
            </div>
          </div>
          <div className="bg-primary/5 dark:bg-primary/10 p-4 text-center border-t border-primary/10 dark:border-primary/20">
            <p className="text-xs text-slate-500 dark:text-slate-400 flex items-center justify-center gap-1">
              <span className="material-symbols-outlined text-[16px]">verified_user</span>
              HIPAA Compliant & Secure
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}