# GitHub Spark Quick Start Guide for IRH Interactive Console

**TL;DR:** Copy the full `GITHUB_SPARK_INTERACTIVE_CONSOLE_PROMPT.md` into GitHub Spark to generate the complete webapp.

---

## 🚀 One-Command Deployment

### For GitHub Spark:

```
Input the entire GITHUB_SPARK_INTERACTIVE_CONSOLE_PROMPT.md file with this instruction:

"Build a production-ready React + TypeScript + FastAPI interactive console 
following this comprehensive specification. Include all components, WebSocket 
integration, Three.js 3D visualization, real-time logging, and comprehensive 
testing. Make it deployable with Docker."
```

---

## 📋 Essential Features Checklist

When GitHub Spark generates the webapp, verify these critical features:

### ✅ Must-Have (Priority 1)
- [ ] **Dashboard** with Cosmic Fixed Point, α⁻¹, w₀ cards
- [ ] **RG Flow Viewer** with 3D trajectory visualization (Three.js)
- [ ] **WebSocket** connection to `/ws/computation` endpoint
- [ ] **Transparency Log** streaming from SSE `/api/v1/stream/logs`
- [ ] **Observable Tracker** showing live constant derivations
- [ ] **Equation Rendering** with KaTeX/MathJax
- [ ] **Dark Theme** as default with light theme toggle

### 🔄 Should-Have (Priority 2)
- [ ] **3D Group Manifold** visualization (SU(2) × U(1))
- [ ] **Computation Queue Manager** with progress bars
- [ ] **Standard Model Dashboard** showing gauge group emergence
- [ ] **Falsification Dashboard** with 20 testable predictions
- [ ] **Export functionality** (JSON, PNG, LaTeX)
- [ ] **Mobile responsiveness** (breakpoints at 768px, 1024px)

### 🌟 Nice-to-Have (Priority 3)
- [ ] **Jupyter integration** for launching notebooks
- [ ] **Custom computation** submission via Monaco Editor
- [ ] **Video tutorials** embedded in help sections
- [ ] **Multi-user sessions** with authentication
- [ ] **GPU toggle** for backend acceleration
- [ ] **HPC cluster** integration

---

## 🏗️ Expected File Structure

GitHub Spark should generate:

```
irh-console/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Dashboard/
│   │   │   │   ├── DashboardView.tsx
│   │   │   │   ├── MetricCard.tsx
│   │   │   │   └── ComputationHistory.tsx
│   │   │   ├── RGFlowViewer/
│   │   │   │   ├── RGFlowViewer.tsx
│   │   │   │   ├── ThreeJSScene.tsx
│   │   │   │   ├── ControlPanel.tsx
│   │   │   │   └── ProgressDisplay.tsx
│   │   │   ├── ObservableTracker/
│   │   │   │   ├── ObservableTracker.tsx
│   │   │   │   ├── AlphaInversePanel.tsx
│   │   │   │   └── ConstantTable.tsx
│   │   │   ├── TransparencyLog/
│   │   │   │   ├── LogViewer.tsx
│   │   │   │   ├── LogEntry.tsx
│   │   │   │   └── LogFilter.tsx
│   │   │   ├── ManifoldViz/
│   │   │   │   ├── ManifoldViz.tsx
│   │   │   │   └── SU2Torus.tsx
│   │   │   ├── QueueManager/
│   │   │   │   ├── QueueManager.tsx
│   │   │   │   └── TaskRow.tsx
│   │   │   ├── StandardModelDashboard/
│   │   │   │   └── StandardModelDashboard.tsx
│   │   │   └── FalsificationDashboard/
│   │   │       └── FalsificationDashboard.tsx
│   │   ├── services/
│   │   │   ├── api.ts              # REST API client
│   │   │   ├── websocket.ts        # WebSocket client
│   │   │   └── sse.ts              # SSE client
│   │   ├── store/
│   │   │   ├── index.ts            # Zustand store
│   │   │   ├── computationSlice.ts
│   │   │   ├── logSlice.ts
│   │   │   └── uiSlice.ts
│   │   ├── types/
│   │   │   ├── api.ts              # API types
│   │   │   ├── computation.ts      # Computation types
│   │   │   └── websocket.ts        # WebSocket event types
│   │   ├── utils/
│   │   │   ├── formatters.ts       # Number/equation formatters
│   │   │   └── validators.ts       # Input validation
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── public/
│   │   └── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── README.md
│
├── backend/
│   ├── app_extended.py             # Extended FastAPI app with WebSocket
│   ├── websocket_handler.py        # WebSocket event handlers
│   ├── sse_handler.py              # SSE log streaming
│   ├── queue_manager.py            # Computation queue
│   ├── background_tasks.py         # Celery/RQ tasks
│   ├── requirements.txt
│   └── README.md
│
├── docker/
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   ├── docker-compose.yml
│   └── nginx.conf
│
├── tests/
│   ├── frontend/
│   │   └── (Jest tests)
│   └── backend/
│       └── (Pytest tests)
│
└── README.md
```

---

## 🔧 Configuration Variables

### Frontend `.env`

```bash
VITE_API_BASE_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws
VITE_SSE_URL=http://localhost:8000/api/v1/stream/logs
VITE_ENABLE_3D=true
VITE_LOG_BUFFER_SIZE=10000
VITE_DEFAULT_THEME=dark
```

### Backend `.env`

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# WebSocket
WS_MAX_CONNECTIONS=100
WS_HEARTBEAT_INTERVAL=30

# Computation Queue
QUEUE_BACKEND=redis
REDIS_URL=redis://localhost:6379/0
MAX_CONCURRENT_TASKS=10
TASK_TIMEOUT=3600

# Logging
LOG_LEVEL=INFO
TRANSPARENCY_ENGINE_VERBOSITY=4

# Performance
ENABLE_GPU=false
ENABLE_MPI=false
MPI_PROCESSES=4
```

---

## 🎨 Color Palette Reference

For custom styling or branding:

```css
/* IRH Console Dark Theme */
--bg-primary: #0a0e27;      /* Deep space blue */
--bg-secondary: #1a1f3a;    
--bg-tertiary: #2a2f4a;     
--text-primary: #e8e8e8;    
--text-secondary: #a0a0a0;  
--accent-quantum: #00d4ff;  /* Quantum blue */
--accent-energy: #ff6b9d;   /* Energy pink */
--accent-gold: #ffd700;     /* Fixed point gold */
--success: #00ff88;         
--warning: #ffaa00;         
--error: #ff4444;           
```

---

## 🧪 Testing Workflow

### Frontend Tests

```bash
cd frontend
npm test                    # Run all Jest tests
npm run test:watch         # Watch mode
npm run test:coverage      # Coverage report
npm run test:e2e           # Cypress E2E tests
```

### Backend Tests

```bash
cd backend
pytest tests/              # Run all tests
pytest tests/ -v           # Verbose
pytest tests/ --cov        # Coverage
pytest tests/ -k websocket # Specific tests
```

### Integration Tests

```bash
docker-compose up -d       # Start all services
npm run test:integration   # Run integration tests
docker-compose down        # Stop services
```

---

## 🚢 Deployment Options

### Option 1: Docker Compose (Recommended for Local)

```bash
# Clone repository
git clone https://github.com/brandonmccraryresearch-cloud/Intrinsic_Resonance_Holography.git
cd Intrinsic_Resonance_Holography

# Build and start
docker-compose up -d

# Access at http://localhost:3000
```

### Option 2: Kubernetes (Production)

```bash
# Apply Kubernetes configs
kubectl apply -f deploy/kubernetes/

# Check status
kubectl get pods -n irh-console

# Access via ingress
# https://irh-console.example.com
```

### Option 3: Cloud Run (Serverless)

```bash
# Build and deploy to Google Cloud Run
gcloud run deploy irh-console \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 📚 Key API Endpoints

### REST API (Existing)

```
GET  /health                          → Health check
GET  /api/v1/fixed-point              → Cosmic Fixed Point
GET  /api/v1/beta-functions           → Beta functions
POST /api/v1/rg-flow/integrate        → Integrate RG flow
GET  /api/v1/observables/alpha        → α⁻¹ calculation
GET  /api/v1/observables/C_H          → Universal exponent
GET  /api/v1/topology/betti           → β₁ = 12
GET  /api/v1/topology/instanton       → n_inst = 3
GET  /api/v1/standard-model/gauge     → Gauge group
GET  /api/v1/cosmology/dark-energy    → w₀
GET  /api/v1/falsifiable/liv          → LIV parameter
GET  /api/v1/neutrinos/masses         → Neutrino masses
GET  /api/v1/neutrinos/hierarchy      → Mass ordering
```

### WebSocket (New)

```
WS   /ws/computation                  → Real-time updates
     Events: progress_update, log_message, task_complete, task_error
```

### Server-Sent Events (New)

```
GET  /api/v1/stream/logs              → Live log streaming
     Events: log, progress, error
```

---

## 🎯 Usage Examples

### Example 1: Start RG Flow Integration

**Frontend (React):**
```typescript
import { useWebSocket } from './hooks/useWebSocket';

function RGFlowViewer() {
  const { send, messages } = useWebSocket('ws://localhost:8000/ws/computation');
  
  const startIntegration = () => {
    send({
      type: 'submit_task',
      data: {
        task_type: 'rg_flow',
        parameters: {
          initial_couplings: [50, 100, 150],
          t_range: [-10, 10],
          solver: 'Radau'
        }
      }
    });
  };
  
  // Handle progress updates
  useEffect(() => {
    const progressMsg = messages.find(m => m.type === 'progress_update');
    if (progressMsg) {
      setProgress(progressMsg.data.progress);
      setCurrentCouplings(progressMsg.data.metrics);
    }
  }, [messages]);
  
  return (
    <button onClick={startIntegration}>
      Start Integration
    </button>
  );
}
```

### Example 2: Stream Transparency Logs

**Frontend (React):**
```typescript
import { useServerSentEvents } from './hooks/useSSE';

function TransparencyLog() {
  const { events } = useServerSentEvents('http://localhost:8000/api/v1/stream/logs');
  
  return (
    <div className="log-viewer">
      {events.map(event => (
        <LogEntry 
          key={event.timestamp}
          level={event.level}
          message={event.message}
          reference={event.reference}
          equation={event.equation_latex}
        />
      ))}
    </div>
  );
}
```

### Example 3: Render 3D Manifold

**Frontend (React Three Fiber):**
```typescript
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';

function ManifoldViz() {
  return (
    <Canvas camera={{ position: [0, 0, 5] }}>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      
      {/* SU(2) torus */}
      <SU2Torus 
        subdivision={64}
        colorMap="holonomic_phase"
      />
      
      {/* U(1) phase circle */}
      <U1Circle radius={0.1} />
      
      {/* Fixed point marker */}
      <mesh position={[0, 0, 0]}>
        <sphereGeometry args={[0.1]} />
        <meshStandardMaterial color="gold" />
      </mesh>
      
      <OrbitControls />
    </Canvas>
  );
}
```

---

## 🐛 Troubleshooting

### Issue: WebSocket not connecting

**Solution:**
```bash
# Check backend is running
curl http://localhost:8000/health

# Check WebSocket endpoint
wscat -c ws://localhost:8000/ws/computation

# Verify CORS settings in backend/.env
ALLOWED_ORIGINS=http://localhost:3000
```

### Issue: Three.js scene not rendering

**Solution:**
```typescript
// Ensure Canvas has dimensions
<Canvas style={{ width: '100%', height: '600px' }}>
  ...
</Canvas>

// Check browser WebGL support
const gl = document.createElement('canvas').getContext('webgl');
console.log('WebGL supported:', !!gl);
```

### Issue: LaTeX equations not rendering

**Solution:**
```bash
# Install KaTeX
npm install katex react-katex

# Import CSS in main.tsx
import 'katex/dist/katex.min.css';
```

### Issue: High memory usage in log viewer

**Solution:**
```typescript
// Implement virtual scrolling
import { FixedSizeList } from 'react-window';

<FixedSizeList
  height={600}
  itemCount={logs.length}
  itemSize={50}
  width="100%"
>
  {({ index, style }) => (
    <div style={style}>
      <LogEntry log={logs[index]} />
    </div>
  )}
</FixedSizeList>
```

---

## 📖 Additional Resources

### Documentation
- **IRH v21.4 Manuscript Part 1:** [Link](./Intrinsic-Resonance-Holography-21.4-Part1.md)
- **IRH v21.4 Manuscript Part 2:** [Link](./Intrinsic-Resonance-Holography-21.4-Part2.md)
- **Technical Reference:** [Link](./docs/TECHNICAL_REFERENCE.md)
- **Architecture Overview:** [Link](./docs/architectural_overview.md)

### Libraries Used
- **React:** https://react.dev/
- **Three.js:** https://threejs.org/
- **D3.js:** https://d3js.org/
- **FastAPI:** https://fastapi.tiangolo.com/
- **Socket.io:** https://socket.io/
- **KaTeX:** https://katex.org/

### Community
- **GitHub Discussions:** Ask questions and share ideas
- **Issue Tracker:** Report bugs or request features
- **Wiki:** Extended documentation and tutorials

---

## ✅ Final Checklist Before Launch

- [ ] Frontend builds without errors (`npm run build`)
- [ ] Backend starts successfully (`uvicorn app:app`)
- [ ] WebSocket connection established
- [ ] SSE stream working
- [ ] All API endpoints return 200 OK
- [ ] Three.js scenes render at 60 FPS
- [ ] Logs display equation references
- [ ] Dashboard metrics update in real-time
- [ ] Mobile responsive (test on 375px width)
- [ ] Dark theme looks correct
- [ ] No console errors in browser
- [ ] Docker image builds successfully
- [ ] All tests pass (`npm test && pytest`)

---

**🎉 You're Ready!**

Copy the `GITHUB_SPARK_INTERACTIVE_CONSOLE_PROMPT.md` into GitHub Spark and let it generate your production-ready IRH Interactive Console!

For questions or issues, refer to:
- Full specification: `GITHUB_SPARK_INTERACTIVE_CONSOLE_PROMPT.md`
- Technical docs: `docs/TECHNICAL_REFERENCE.md`
- Repository: https://github.com/brandonmccraryresearch-cloud/Intrinsic_Resonance_Holography

---

*Last Updated: January 2026*  
*Version: 1.0*  
*Author: IRH Development Team*
