/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "templates/*.{html,js}",
        "templates/**/*.{html,js}"
    ],
    theme: {
        borderWidth: {
            DEFAULT: '1px',
            '0': '0',
            's': '0.5px',
            '2': '2px',
            '3': '3px',
            '4': '4px',
            '6': '6px',
            '8': '8px',
        },
        extend: {
            screens: {
                'xs': { 'min': '0px' },
                'sm': { 'min': '640px' },
                'md': { 'min': '768px' },
                'lg': { 'min': '1024px' },
                'xl': { 'min': '1280px' },
            },
            dropShadow: {
                '3xl': '0 35px 35px rgba(0, 0, 0, 0.25)',
                '4xl': [
                    '0 35px 35px rgba(0, 0, 0, 0.25)',
                    '0 45px 65px rgba(0, 0, 0, 0.15)'
                ],
                'neo-light-icon': [
                    '4px 4px 8px #B9CCE7',
                    '-4px -4px 8px rgba(255, 255, 255, 0.8)'
                ],
                'neo-dark-icon': [
                    '9px 9px 16px rgba(0, 0, 0, 0.4)',
                    '-9px -9px 16px rgba(73, 73, 73, 0.6)'
                ],
                'neo-light-button': [
                    '-4px -4px 8px #FFFFFF',
                    '4px 4px 8px rgba(174, 174, 192, 0.5)'
                ],
                'neo-dark-button': [
                    '-4px -4px 8px #3E3E3E',
                    '4px 4px 8px #1E1E1E'
                ],
                'neo-light-portfolio-button': [
                    '-2px -2px 4px #BAD8FF',
                    '2px 2px 4px #A6A5EE'
                ],

            },
            colors: {
                'blue': '#1fb6ff',
                'purple': '#7e5bef',
                'pink': '#ff49db',
                'orange': '#ff7849',
                'green': '#13ce66',
                'yellow': '#ffc82c',
                'gray-dark': '#273444',
                'gray': '#8492a6',
                'gray-light': '#d3dce6',
                'custom': {
                    'light': '#F0F0F3',
                    'primary': '#0193FD',
                    'blue-1': '#5A90E1',
                    'blue-2': '#29B1FD',
                    'dark': '#333333',
                    'gradient-blue': '#93CDED',
                    'gradient-active-blue': '#A0B2EE',
                    'gradient-purple': '#B386ED'
                }
            },
            fontFamily: {
                sans: ['Graphik', 'sans-serif'],
                serif: ['Merriweather', 'serif'],
            },
            extend: {
                spacing: {
                    '128': '32rem',
                    '144': '36rem',
                },
                borderRadius: {
                    '4xl': '2rem',
                }
            }
        },
    },
    plugins: [],
}