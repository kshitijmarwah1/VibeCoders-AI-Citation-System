# VibeVerifier Frontend

Modern, interactive frontend for the AI Hallucination & Citation Verification System built with Next.js, React, TypeScript, Tailwind CSS, and ShadCN UI.

## Features

- 🎨 **Modern Dark UI** with neon accents (cyan, pink, purple)
- 🌈 **Animated Gradient Background** for a soothing visual experience
- 📝 **Multi-Format Input Support** (Text, URL, File upload)
- 🎯 **Dynamic Input UI** that changes based on selected format
- 🖱️ **Drag & Drop** file upload support
- 📊 **Interactive Results Display** with detailed claim analysis
- ⚡ **Real-time Verification** with loading states
- 🎭 **ShadCN UI Components** for consistent design

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Backend API running (default: http://127.0.0.1:8000)

### Installation

1. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

2. Create a `.env.local` file (optional):
```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

3. Run the development server:
```bash
npm run dev
# or
yarn dev
# or
pnpm dev
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Main page
│   └── globals.css         # Global styles
├── components/
│   ├── ui/                 # ShadCN UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── progress.tsx
│   │   └── tabs.tsx
│   ├── Navbar.tsx          # Navigation bar
│   ├── AnimatedGradient.tsx # Animated background
│   ├── InputArea.tsx       # Input area with format selection
│   └── ResultsDisplay.tsx  # Results visualization
└── lib/
    └── utils.ts            # Utility functions
```

## Components

### Navbar
Fixed navigation bar with branding and system status indicator.

### AnimatedGradient
Animated gradient background with pulsing orbs and mesh effects.

### InputArea
- Format selection buttons (Text, URL, File)
- Dynamic input UI based on selection
- Drag & drop file upload
- File preview and management

### ResultsDisplay
- Overall reliability score
- Individual claim analysis
- Confidence, similarity, and credibility metrics
- Citation links
- Status indicators (verified/hallucinated)

## API Integration

The frontend communicates with the backend API endpoints:

- `POST /verify/text` - Verify text content
- `POST /verify/url` - Verify URL content
- `POST /verify/file` - Verify file upload (PDF/DOCX)

## Styling

The UI uses:
- **Dark theme** with black background
- **Neon accents**: Cyan (#22d3ee), Pink (#ec4899), Purple (#a855f7)
- **Glassmorphism** effects with backdrop blur
- **Smooth animations** and transitions
- **Custom scrollbar** styling

## Technologies

- **Next.js 16** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS 4** - Utility-first CSS
- **ShadCN UI** - Component library
- **Radix UI** - Accessible primitives
- **Lucide React** - Icons
- **Class Variance Authority** - Component variants

## Build for Production

```bash
npm run build
npm start
```

## License

Part of the VibeVerifier project.
