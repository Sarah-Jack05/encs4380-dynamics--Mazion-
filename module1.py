import numpy as np
import matplotlib.pyplot as plt
from pyscript import document, display, when

# ==================================================
# 1. الدوال الرياضية الأساسية
# ==================================================
def calculate_step_response(K, tau, t, A=1.0):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return K * A * (1 - np.exp(-np.asarray(t) / tau))

def calculate_ramp_response(K, tau, t, A=1.0):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return K * A * (np.asarray(t) - tau + tau * np.exp(-np.asarray(t) / tau))

def calculate_important_points(K, tau, A=1.0):
    t1 = tau
    y1 = calculate_step_response(K, tau, t1, A)
    t2 = 3 * tau
    y2 = calculate_step_response(K, tau, t2, A)
    return (t1, y1), (t2, y2)

def calculate_ramp_lag(tau):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return tau

def calculate_steady_state_error(K, tau, A=1.0):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return K * A * tau

def calculate_error_fraction(tau, t):
    if tau <= 0:
        raise ValueError("Time constant must be positive")
    return np.exp(-np.asarray(t) / tau)

# ==================================================
# 2. دالة التحديث التفاعلي مع صفحة الويب
# ==================================================
def update_simulation(event=None):
    # قراءة القيم الحالية من الصفحة
    K = float(document.querySelector("#k").value)
    tau = float(document.querySelector("#tau").value)
    is_step = document.querySelector("#step").checked
    
    # التحقق من وجود زر الخطأ في الصفحة
    error_checkbox = document.querySelector("#error")
    show_error = error_checkbox.checked if error_checkbox else False

    # تحديث أرقام أشرطة التمرير
    document.querySelector("#k_out").innerText = f"{K:.1f}"
    document.querySelector("#tau_out").innerText = f"{tau:.1f}"

    # حساب وعرض القيم الرقمية
    (t1, y1), (t2, y2) = calculate_important_points(K, tau)
    ramp_lag = calculate_ramp_lag(tau)
    sse = calculate_steady_state_error(K, tau)

    document.querySelector("#val_tau").innerText = f"{y1:.3f}"
    document.querySelector("#val_3tau").innerText = f"{y2:.3f}"
    document.querySelector("#val_ramp_lag").innerText = f"{ramp_lag:.2f} s"
    document.querySelector("#val_sse").innerText = f"{sse:.2f}"

    # تجهيز محور الزمن
    t_max = max(15.0, 5 * tau)
    t = np.linspace(0, t_max, 500)

    # إنشاء الرسم الأساسي (Step أو Ramp)
    fig, ax = plt.subplots(figsize=(8, 4.5))

    if is_step:
        y = calculate_step_response(K, tau, t)
        final_value = K * 1.0
        ax.plot(t, y, linewidth=2.5, label="System Output")
        ax.scatter([t1, t2], [y1, y2], color="red", zorder=5, label=f"63.2% at t={tau:.1f}s")
        ax.scatter([t2], [y2], color="green", zorder=5, label=f"95% at t={3*tau:.1f}s")
        ax.axhline(final_value, linestyle="--", color="gray", label="Final Value")
        ax.axvline(tau, linestyle="--", alpha=0.5)
        ax.axvline(3 * tau, linestyle="--", alpha=0.5)
        ax.set_title("First-Order System: Step Response")
        ax.set_ylabel("Output y(t)")
    else:
        y = calculate_ramp_response(K, tau, t)
        ax.plot(t, t, "--", linewidth=2, color="gray", label="Reference Input")
        ax.plot(t, y, linewidth=2.5, color="green", label="System Output")
        ax.set_title("First-Order System: Ramp Response and Ramp Lag")
        ax.set_ylabel("Amplitude")

    ax.set_xlabel("Time (seconds)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    plt.tight_layout()

    # تفريغ الرسم القديم وعرض الرسم الجديد في plot1
    plot_div = document.querySelector("#plot1")
    plot_div.innerHTML = ""
    display(fig, target="plot1")
    plt.close(fig)

    # التعامل مع الرسم اللوغاريتمي لنسبة الخطأ (plot1_error)
    error_div = document.querySelector("#plot1_error")
    if error_div:
        if show_error:
            error_div.removeAttribute("hidden")
            fig_err, ax_err = plt.subplots(figsize=(8, 4.5))
            err_frac = calculate_error_fraction(tau, t)
            ax_err.plot(t, err_frac, linewidth=2.5, color="purple", label=r"$e(t)/e(0)=e^{-t/\tau}$")
            ax_err.set_yscale("log")
            ax_err.set_xlabel("Time (seconds)")
            ax_err.set_ylabel("Error Fraction (log scale)")
            ax_err.set_title("First-Order Error Fraction - Logarithmic Scale")
            ax_err.grid(True, which="both", alpha=0.3)
            ax_err.legend()
            plt.tight_layout()

            error_div.innerHTML = ""
            display(fig_err, target="plot1_error")
            plt.close(fig_err)
        else:
            error_div.setAttribute("hidden", "")

# ==================================================
# 3. ربط التحديث بحركة المستخدم في الصفحة
# ==================================================
@when("input", "#k")
@when("input", "#tau")
@when("change", "#step")
@when("change", "#ramp")
@when("change", "#error")
def on_input_change(event):
    update_simulation()

# التشغيل الأولي عند فتح الموقع
update_simulation()
