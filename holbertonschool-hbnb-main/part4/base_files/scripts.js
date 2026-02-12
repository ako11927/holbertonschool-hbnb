// scripts.js
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            // الحصول على البريد الإلكتروني وكلمة المرور
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            // عنصر عرض الخطأ
            const errorDiv = document.getElementById('error-message');

            // مسح أي رسالة خطأ سابقة
            errorDiv.style.display = 'none';
            errorDiv.innerText = '';

            try {
                // إرسال الطلب إلى API
                const response = await fetch('http://localhost:5000/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password }),
                    credentials: 'include'
                });

                const data = await response.json();

                if (response.ok) {
                    // تخزين JWT في كوكي
                    document.cookie = `token=${data.access_token}; path=/; max-age=3600; SameSite=Lax`;
                    
                    // تحويل المستخدم إلى الصفحة الرئيسية
                    window.location.href = 'index.html';
                } else {
                    // عرض رسالة الخطأ
                    errorDiv.innerText = data.message || 'Login failed. Please check your credentials.';
                    errorDiv.style.display = 'block';
                }
            } catch (error) {
                // خطأ في الشبكة أو الاتصال
                errorDiv.innerText = 'Network error. Please try again later.';
                errorDiv.style.display = 'block';
                console.error('Login error:', error);
            }
        });
    }
});