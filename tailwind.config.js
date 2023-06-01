/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{html,js,css}",
    './your_weather/**/*.{html,js,css}',
    './site/**/*.{html,js,css}',
    './app/templates/base.html',
    "./node_modules/flowbite/**/*.js"

  ],
  
  theme: {
    extend: {},
  },
  plugins: [        
    require("flowbite/plugin")
],
}

