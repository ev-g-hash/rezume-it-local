// Тур по сайту - интерактивное руководство

(function() {
    'use strict';
    
    const Tour = {
        currentStep: 0,
        steps: [],
        isMobile: window.innerWidth < 768,
        
        // Шаги тура
        initSteps: function() {
            this.steps = [
                {
                    element: null,
                    title: '👋 Привет!',
                    message: 'Я ваш путеводитель по резюме. Нажмите "Начать", чтобы начать экскурсию.',
                    isWelcome: true
                },
                {
                    element: '#nav-about',
                    title: '📋 Обо мне',
                    message: 'Здесь вы узнаете о моих навыках, опыте работы и профессиональном пути.',
                    position: 'bottom'
                },
                {
                    element: '#nav-certificates',
                    title: '🎓 Сертификаты',
                    message: 'Здесь вы узнаете о моих курсах, дипломах и профессиональных сертификатах.',
                    position: 'bottom'
                },
                {
                    element: '#nav-projects',
                    title: '💼 Проекты',
                    message: 'Здесь вы узнаете о моих готовых проектах. Демо-версии доступны по телефону: 8-908-859-50-09',
                    position: 'bottom'
                }
            ];
        },
        
        // Показать приветственное модальное окно
        showWelcome: function() {
            const modal = document.getElementById('tour-welcome-modal');
            if (modal) {
                modal.classList.add('active');
            }
        },
        
        hideWelcome: function() {
            const modal = document.getElementById('tour-welcome-modal');
            if (modal) {
                modal.classList.remove('active');
            }
        },
        
        // Показать определенный шаг
        showStep: function(stepIndex) {
            if (stepIndex >= this.steps.length) {
                this.finish();
                return;
            }
            
            const step = this.steps[stepIndex];
            
            // Если это приветственный шаг
            if (step.isWelcome) {
                this.showWelcome();
                return;
            }
            
            this.hideWelcome();
            
            // На мобильных - открываем меню если закрыто
            if (this.isMobile) {
                const navbarToggler = document.querySelector('.navbar-toggler');
                const navbarCollapse = document.querySelector('#navbarNav');
                if (navbarToggler && navbarCollapse && !navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            }
            
            // Показываем подсказку
            this.showTooltip(step, stepIndex);
        },
        
        // Показать тултип с подсказкой
        showTooltip: function(step, stepIndex) {
            let tooltip = document.getElementById('tour-tooltip');
            if (!tooltip) {
                tooltip = this.createTooltip();
            }
            
            // Находим целевой элемент
            let targetElement = null;
            if (step.element) {
                targetElement = document.querySelector(step.element);
            }
            
            if (targetElement) {
                const rect = targetElement.getBoundingClientRect();
                const tooltipRect = tooltip.getBoundingClientRect();
                
                // Позиционируем тултип
                let left = rect.left + rect.width / 2 - tooltipRect.width / 2;
                let top = rect.bottom + 20;
                
                // Корректировка для мобильных
                if (this.isMobile) {
                    left = 20;
                    top = rect.bottom + 15;
                }
                
                // Проверяем выход за границы экрана
                if (left < 20) left = 20;
                if (left + tooltipRect.width > window.innerWidth - 20) {
                    left = window.innerWidth - tooltipRect.width - 20;
                }
                
                // Если низ экрана недоступен, показываем сверху
                if (top + tooltipRect.height > window.innerHeight - 50) {
                    top = rect.top - tooltipRect.height - 20;
                    // Меняем направление стрелки
                    tooltip.style.setProperty('--arrow-direction', 'down');
                } else {
                    tooltip.style.setProperty('--arrow-direction', 'up');
                }
                
                tooltip.style.left = left + 'px';
                tooltip.style.top = top + 'px';
                
                // Подсвечиваем элемент
                targetElement.classList.add('tour-highlight');
            } else {
                // Если элемент не найден, показываем в центре
                tooltip.style.left = '50%';
                tooltip.style.top = '50%';
                tooltip.style.transform = 'translate(-50%, -50%)';
            }
            
            // Обновляем контент
            const titleEl = tooltip.querySelector('.tour-tooltip-title');
            const messageEl = tooltip.querySelector('.tour-tooltip-message');
            
            if (titleEl) titleEl.textContent = step.title;
            if (messageEl) messageEl.textContent = step.message;
            
            // Показываем тултип
            tooltip.classList.add('active');
            
            // Обновляем прогресс
            this.updateProgress(stepIndex);
            
            // Показываем стрелку
            this.showArrow(targetElement);
            
            // Автоматический переход через 3 секунды
            setTimeout(() => {
                this.nextStep();
            }, 3000);
        },
        
        // Создать элемент тултипа
        createTooltip: function() {
            const tooltip = document.createElement('div');
            tooltip.id = 'tour-tooltip';
            tooltip.className = 'tour-tooltip';
            tooltip.innerHTML = `
                <button class="tour-tooltip-close" onclick="Tour.skip()">&times;</button>
                <div class="tour-tooltip-content">
                    <div class="tour-tooltip-icon">
                        <i class="fas fa-info"></i>
                    </div>
                    <div class="tour-tooltip-text">
                        <h4 class="tour-tooltip-title"></h4>
                        <p class="tour-tooltip-message"></p>
                    </div>
                </div>
            `;
            document.body.appendChild(tooltip);
            return tooltip;
        },
        
        // Показать стрелку
        showArrow: function(targetElement) {
            let arrow = document.getElementById('tour-arrow');
            if (!arrow) {
                arrow = document.createElement('div');
                arrow.id = 'tour-arrow';
                arrow.className = 'tour-arrow';
                arrow.innerHTML = `
                    <svg viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 4l-8 8h5v8h6v-8h5z"/>
                    </svg>
                `;
                document.body.appendChild(arrow);
            }
            
            if (targetElement) {
                const rect = targetElement.getBoundingClientRect();
                arrow.style.left = (rect.left + rect.width / 2 - 30) + 'px';
                arrow.style.top = (rect.bottom + 10) + 'px';
                arrow.classList.add('active');
            }
        },
        
        // Скрыть стрелку
        hideArrow: function() {
            const arrow = document.getElementById('tour-arrow');
            if (arrow) {
                arrow.classList.remove('active');
            }
        },
        
        // Обновить прогресс
        updateProgress: function(stepIndex) {
            const progressContainer = document.getElementById('tour-progress');
            if (!progressContainer) return;
            
            const dots = progressContainer.querySelectorAll('.tour-progress-dot');
            dots.forEach((dot, index) => {
                dot.classList.remove('active', 'completed');
                if (index < stepIndex) {
                    dot.classList.add('completed');
                } else if (index === stepIndex) {
                    dot.classList.add('active');
                }
            });
        },
        
        // Создать индикатор прогресса
        createProgress: function() {
            const container = document.createElement('div');
            container.id = 'tour-progress';
            container.className = 'tour-progress';
            
            for (let i = 0; i < this.steps.length; i++) {
                const dot = document.createElement('div');
                dot.className = 'tour-progress-dot';
                if (i === 0) dot.classList.add('active');
                container.appendChild(dot);
            }
            
            document.body.appendChild(container);
        },
        
        // Переход к следующему шагу
        nextStep: function() {
            this.currentStep++;
            if (this.currentStep >= this.steps.length) {
                this.finish();
            } else {
                this.showStep(this.currentStep);
            }
        },
        
        // Пропустить тур
        skip: function() {
            this.hideAll();
            // Сохраняем в localStorage что тур завершен
            localStorage.setItem('tour-completed', 'true');
        },
        
        // Завершить тур
        finish: function() {
            this.hideAll();
            localStorage.setItem('tour-completed', 'true');
            
            // Показываем сообщение об окончании
            const tooltip = document.getElementById('tour-tooltip');
            if (tooltip) {
                tooltip.querySelector('.tour-tooltip-title').textContent = '🎉 Готово!';
                tooltip.querySelector('.tour-tooltip-message').textContent = 'Теперь вы знаете о структуре резюме. Приятного просмотра!';
                tooltip.style.left = '50%';
                tooltip.style.top = '50%';
                tooltip.style.transform = 'translate(-50%, -50%)';
                tooltip.classList.add('active');
                
                setTimeout(() => {
                    tooltip.classList.remove('active');
                }, 3000);
            }
        },
        
        // Скрыть все элементы тура
        hideAll: function() {
            this.hideWelcome();
            
            const tooltip = document.getElementById('tour-tooltip');
            if (tooltip) {
                tooltip.classList.remove('active');
            }
            
            this.hideArrow();
            
            // Убираем подсветку
            document.querySelectorAll('.tour-highlight').forEach(el => {
                el.classList.remove('tour-highlight');
            });
            
            // Убираем индикатор прогресса
            const progress = document.getElementById('tour-progress');
            if (progress) {
                progress.remove();
            }
        },
        
        // Инициализация тура
        init: function() {
            // Проверяем, не завершался ли уже тур
            if (localStorage.getItem('tour-completed')) {
                return;
            }
            
            this.initSteps();
            this.createProgress();
            
            // Показываем приветственное окно через небольшую задержку
            setTimeout(() => {
                this.showStep(0);
            }, 500);
            
            // Обработчик кнопки запуска тура
            const startBtn = document.getElementById('tour-start-btn');
            if (startBtn) {
                startBtn.addEventListener('click', () => {
                    this.nextStep();
                });
            }
        }
    };
    
    // Глобальный доступ
    window.Tour = Tour;
    
    // Запуск при загрузке DOM
    document.addEventListener('DOMContentLoaded', function() {
        Tour.init();
    });
    
    // Обновление при изменении размера окна
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(function() {
            Tour.isMobile = window.innerWidth < 768;
            // Перезапускаем текущий шаг если тур активен
            const tooltip = document.getElementById('tour-tooltip');
            if (tooltip && tooltip.classList.contains('active')) {
                Tour.showStep(Tour.currentStep);
            }
        }, 250);
    });
    
})();