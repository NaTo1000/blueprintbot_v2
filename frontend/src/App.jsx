import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom'
import { 
  Upload, 
  FileText, 
  Zap, 
  Brain, 
  Cpu, 
  Activity, 
  Settings, 
  Download, 
  Eye, 
  BarChart3, 
  PieChart, 
  TrendingUp, 
  CheckCircle, 
  AlertCircle, 
  Clock, 
  Users, 
  Building, 
  Layers, 
  Ruler, 
  Calculator, 
  Sparkles, 
  Atom, 
  Infinity,
  Menu,
  X,
  Home,
  Database,
  Cloud,
  Shield,
  Gauge,
  Workflow,
  Lightbulb,
  Target,
  Rocket,
  Globe,
  Star,
  ChevronRight,
  Play,
  Pause,
  Square,
  RotateCcw,
  Save,
  Share2,
  Filter,
  Search,
  Bell,
  User,
  LogOut,
  HelpCircle,
  ExternalLink,
  ArrowUpRight,
  ChevronDown,
  Plus,
  Minus,
  Maximize2,
  Minimize2,
  MoreHorizontal,
  RefreshCw,
  Trash2,
  Edit3,
  Copy,
  FolderOpen,
  Image,
  Video,
  FileImage,
  FileVideo,
  Mic,
  Camera,
  Palette,
  Code,
  Terminal,
  GitBranch,
  Package,
  Layers3,
  Boxes,
  Network,
  Server,
  MonitorSpeaker,
  Headphones,
  Volume2,
  VolumeX,
  Wifi,
  WifiOff,
  Battery,
  BatteryLow,
  Bluetooth,
  Usb,
  HardDrive,
  MemoryStick,
  ScanLine,
  QrCode,
  Fingerprint,
  Lock,
  Unlock,
  Key,
  ShieldCheck,
  AlertTriangle,
  Info,
  MessageSquare,
  Mail,
  Phone,
  MapPin,
  Calendar,
  Clock3,
  Timer,
  Stopwatch,
  AlarmClock,
  Sun,
  Moon,
  CloudRain,
  CloudSnow,
  Wind,
  Thermometer,
  Droplets,
  Flame,
  Snowflake,
  Zap as Lightning,
  Flashlight,
  Lightbulb as Bulb,
  Lamp,
  Candle
} from 'lucide-react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Label } from '@/components/ui/label.jsx'
import { Textarea } from '@/components/ui/textarea.jsx'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select.jsx'
import { Switch } from '@/components/ui/switch.jsx'
import { Slider } from '@/components/ui/slider.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar.jsx'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuTrigger } from '@/components/ui/dropdown-menu.jsx'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog.jsx'
import { Alert, AlertDescription, AlertTitle } from '@/components/ui/alert.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip.jsx'
import { 
  LineChart, 
  Line, 
  AreaChart, 
  Area, 
  BarChart, 
  Bar, 
  PieChart as RechartsPieChart, 
  Cell, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip as RechartsTooltip, 
  Legend, 
  ResponsiveContainer,
  RadialBarChart,
  RadialBar,
  ScatterChart,
  Scatter,
  ComposedChart,
  ReferenceLine
} from 'recharts'
import './App.css'

// Mock data for demonstrations
const mockAnalysisData = [
  { name: 'Jan', analyses: 45, accuracy: 98.2, efficiency: 92.1 },
  { name: 'Feb', analyses: 52, accuracy: 98.7, efficiency: 94.3 },
  { name: 'Mar', analyses: 48, accuracy: 97.9, efficiency: 91.8 },
  { name: 'Apr', analyses: 61, accuracy: 99.1, efficiency: 95.7 },
  { name: 'May', analyses: 55, accuracy: 98.5, efficiency: 93.2 },
  { name: 'Jun', analyses: 67, accuracy: 99.3, efficiency: 96.4 }
]

const mockQuantumMetrics = [
  { name: 'Coherence', value: 94.7, color: '#8B5CF6' },
  { name: 'Fidelity', value: 97.2, color: '#06B6D4' },
  { name: 'Gate Error', value: 2.1, color: '#EF4444' },
  { name: 'Readout', value: 98.9, color: '#10B981' }
]

const mockBlueprintTypes = [
  { name: 'Architectural', count: 234, percentage: 45.2 },
  { name: 'Structural', count: 156, percentage: 30.1 },
  { name: 'Electrical', count: 89, percentage: 17.2 },
  { name: 'Mechanical', count: 39, percentage: 7.5 }
]

const mockRecentAnalyses = [
  {
    id: '1',
    name: 'Modern Office Complex',
    type: 'Architectural',
    status: 'completed',
    accuracy: 98.7,
    timestamp: '2 hours ago',
    size: '2.4 MB',
    duration: '3m 42s'
  },
  {
    id: '2',
    name: 'Residential Tower',
    type: 'Structural',
    status: 'processing',
    progress: 67,
    timestamp: '15 minutes ago',
    size: '5.1 MB',
    duration: 'In progress'
  },
  {
    id: '3',
    name: 'Shopping Mall Layout',
    type: 'Architectural',
    status: 'completed',
    accuracy: 97.2,
    timestamp: '1 day ago',
    size: '8.7 MB',
    duration: '7m 18s'
  },
  {
    id: '4',
    name: 'Bridge Infrastructure',
    type: 'Structural',
    status: 'failed',
    error: 'Invalid file format',
    timestamp: '2 days ago',
    size: '12.3 MB',
    duration: 'Failed'
  }
]

// Component for animated background
const AnimatedBackground = () => {
  return (
    <div className="fixed inset-0 -z-10 overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-blue-900/20 to-cyan-900/20" />
      <div className="absolute inset-0">
        {[...Array(50)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-1 h-1 bg-white/20 rounded-full"
            style={{
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, -100, 0],
              opacity: [0, 1, 0],
            }}
            transition={{
              duration: Math.random() * 3 + 2,
              repeat: Infinity,
              delay: Math.random() * 2,
            }}
          />
        ))}
      </div>
      <div className="absolute bottom-4 left-4 text-xs text-white/60 font-mono">
        infinite♾2025
      </div>
    </div>
  )
}

// Navigation component
const Navigation = ({ isOpen, setIsOpen }) => {
  const location = useLocation()
  
  const navItems = [
    { path: '/', label: 'Dashboard', icon: Home },
    { path: '/analyze', label: 'Analyze', icon: Zap },
    { path: '/quantum', label: 'Quantum Lab', icon: Atom },
    { path: '/ai-studio', label: 'AI Studio', icon: Brain },
    { path: '/projects', label: 'Projects', icon: FolderOpen },
    { path: '/analytics', label: 'Analytics', icon: BarChart3 },
    { path: '/settings', label: 'Settings', icon: Settings }
  ]

  return (
    <>
      {/* Mobile overlay */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
            onClick={() => setIsOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.div
        initial={{ x: -300 }}
        animate={{ x: isOpen ? 0 : -300 }}
        transition={{ type: 'spring', damping: 25, stiffness: 200 }}
        className="fixed left-0 top-0 h-full w-72 bg-black/90 backdrop-blur-xl border-r border-white/10 z-50 lg:relative lg:translate-x-0"
      >
        <div className="p-6">
          <div className="flex items-center justify-between mb-8">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-cyan-500 rounded-lg flex items-center justify-center">
                <Atom className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">ArciTEK.AI</h1>
                <p className="text-xs text-gray-400">BlueprintBot v2</p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsOpen(false)}
              className="lg:hidden text-white hover:bg-white/10"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>

          <nav className="space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon
              const isActive = location.pathname === item.path
              
              return (
                <Link key={item.path} to={item.path}>
                  <motion.div
                    whileHover={{ x: 4 }}
                    className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                      isActive 
                        ? 'bg-gradient-to-r from-purple-500/20 to-cyan-500/20 text-white border border-purple-500/30' 
                        : 'text-gray-300 hover:text-white hover:bg-white/5'
                    }`}
                  >
                    <Icon className="w-5 h-5" />
                    <span className="font-medium">{item.label}</span>
                    {isActive && (
                      <motion.div
                        layoutId="activeTab"
                        className="ml-auto w-2 h-2 bg-cyan-400 rounded-full"
                      />
                    )}
                  </motion.div>
                </Link>
              )
            })}
          </nav>

          <div className="mt-8 p-4 bg-gradient-to-br from-purple-500/10 to-cyan-500/10 rounded-lg border border-purple-500/20">
            <div className="flex items-center space-x-2 mb-2">
              <Sparkles className="w-4 h-4 text-yellow-400" />
              <span className="text-sm font-medium text-white">Quantum Status</span>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between text-xs">
                <span className="text-gray-400">Coherence</span>
                <span className="text-green-400">94.7%</span>
              </div>
              <Progress value={94.7} className="h-1" />
            </div>
          </div>
        </div>
      </motion.div>
    </>
  )
}

// Header component
const Header = ({ setIsOpen }) => {
  const [notifications, setNotifications] = useState(3)
  
  return (
    <header className="h-16 bg-black/50 backdrop-blur-xl border-b border-white/10 px-6 flex items-center justify-between">
      <div className="flex items-center space-x-4">
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setIsOpen(true)}
          className="lg:hidden text-white hover:bg-white/10"
        >
          <Menu className="w-5 h-5" />
        </Button>
        
        <div className="hidden md:flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
          <span className="text-sm text-gray-300">System Operational</span>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <div className="hidden md:flex items-center space-x-6 text-sm text-gray-300">
          <div className="flex items-center space-x-2">
            <Cpu className="w-4 h-4" />
            <span>CPU: 23%</span>
          </div>
          <div className="flex items-center space-x-2">
            <Activity className="w-4 h-4" />
            <span>Memory: 1.2GB</span>
          </div>
          <div className="flex items-center space-x-2">
            <Atom className="w-4 h-4 text-purple-400" />
            <span>Quantum: Active</span>
          </div>
        </div>

        <Button variant="ghost" size="sm" className="relative text-white hover:bg-white/10">
          <Bell className="w-5 h-5" />
          {notifications > 0 && (
            <span className="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
              {notifications}
            </span>
          )}
        </Button>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button variant="ghost" size="sm" className="text-white hover:bg-white/10">
              <Avatar className="w-8 h-8">
                <AvatarImage src="/api/placeholder/32/32" />
                <AvatarFallback>AI</AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-56">
            <DropdownMenuLabel>My Account</DropdownMenuLabel>
            <DropdownMenuSeparator />
            <DropdownMenuItem>
              <User className="mr-2 h-4 w-4" />
              Profile
            </DropdownMenuItem>
            <DropdownMenuItem>
              <Settings className="mr-2 h-4 w-4" />
              Settings
            </DropdownMenuItem>
            <DropdownMenuItem>
              <HelpCircle className="mr-2 h-4 w-4" />
              Help
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem>
              <LogOut className="mr-2 h-4 w-4" />
              Log out
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  )
}

// Dashboard page component
const Dashboard = () => {
  const [selectedMetric, setSelectedMetric] = useState('analyses')
  
  return (
    <div className="p-6 space-y-6">
      {/* Hero Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-12"
      >
        <motion.h1
          initial={{ scale: 0.9 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2 }}
          className="text-5xl font-bold text-white mb-4"
        >
          Welcome to <span className="bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">ArciTEK.AI</span>
        </motion.h1>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto"
        >
          Revolutionary AI-powered blueprint analysis with quantum computing integration. 
          Transform your architectural and engineering workflows with unprecedented precision and speed.
        </motion.p>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6 }}
          className="flex flex-wrap justify-center gap-4"
        >
          <Button size="lg" className="bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-600 hover:to-cyan-600">
            <Zap className="mr-2 h-5 w-5" />
            Start Analysis
          </Button>
          <Button size="lg" variant="outline" className="border-white/20 text-white hover:bg-white/10">
            <Play className="mr-2 h-5 w-5" />
            Watch Demo
          </Button>
        </motion.div>
      </motion.div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          { title: 'Total Analyses', value: '2,847', change: '+12.5%', icon: FileText, color: 'from-blue-500 to-cyan-500' },
          { title: 'Quantum Operations', value: '1,293', change: '+8.2%', icon: Atom, color: 'from-purple-500 to-pink-500' },
          { title: 'AI Accuracy', value: '98.7%', change: '+0.3%', icon: Brain, color: 'from-green-500 to-emerald-500' },
          { title: 'Processing Speed', value: '3.2s', change: '-15.7%', icon: Zap, color: 'from-yellow-500 to-orange-500' }
        ].map((stat, index) => (
          <motion.div
            key={stat.title}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="bg-black/40 border-white/10 hover:border-white/20 transition-colors">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-400 mb-1">{stat.title}</p>
                    <p className="text-2xl font-bold text-white">{stat.value}</p>
                    <p className="text-sm text-green-400 flex items-center mt-1">
                      <TrendingUp className="w-3 h-3 mr-1" />
                      {stat.change}
                    </p>
                  </div>
                  <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${stat.color} flex items-center justify-center`}>
                    <stat.icon className="w-6 h-6 text-white" />
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.5 }}
        >
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <BarChart3 className="mr-2 h-5 w-5" />
                Analysis Performance
              </CardTitle>
              <CardDescription>Monthly analysis trends and accuracy metrics</CardDescription>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <ComposedChart data={mockAnalysisData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="name" stroke="#9CA3AF" />
                  <YAxis stroke="#9CA3AF" />
                  <RechartsTooltip 
                    contentStyle={{ 
                      backgroundColor: '#1F2937', 
                      border: '1px solid #374151',
                      borderRadius: '8px'
                    }}
                  />
                  <Legend />
                  <Bar dataKey="analyses" fill="#8B5CF6" name="Analyses" />
                  <Line type="monotone" dataKey="accuracy" stroke="#06B6D4" name="Accuracy %" />
                </ComposedChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.6 }}
        >
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Atom className="mr-2 h-5 w-5" />
                Quantum Metrics
              </CardTitle>
              <CardDescription>Real-time quantum computing performance</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mockQuantumMetrics.map((metric, index) => (
                  <div key={metric.name} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-300">{metric.name}</span>
                      <span className="text-white font-medium">{metric.value}%</span>
                    </div>
                    <Progress 
                      value={metric.value} 
                      className="h-2"
                      style={{ '--progress-background': metric.color }}
                    />
                  </div>
                ))}
              </div>
              <div className="mt-6 p-4 bg-gradient-to-r from-purple-500/10 to-cyan-500/10 rounded-lg border border-purple-500/20">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm text-gray-300">Quantum Advantage</p>
                    <p className="text-lg font-bold text-white">847x Faster</p>
                  </div>
                  <Sparkles className="w-8 h-8 text-yellow-400" />
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Real-Time Site Status Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.6 }}
      >
        <Card className="bg-black/40 border-white/10 mb-6">
          <CardHeader>
            <CardTitle className="text-white flex items-center justify-between">
              <div className="flex items-center">
                <Activity className="mr-2 h-5 w-5 text-emerald-400" />
                Real-Time Site Monitoring: {realtimeStatus.siteId}
              </div>
              <div className="flex items-center gap-2">
                <span className="flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span className="text-[10px] text-slate-400 uppercase tracking-wider">Live Sync Active</span>
              </div>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                <p className="text-gray-400 text-xs uppercase mb-1">Current Progress</p>
                <p className="text-2xl font-bold text-emerald-400">{realtimeStatus.progress}%</p>
                <div className="w-full bg-white/10 h-1.5 mt-2 rounded-full overflow-hidden">
                  <div className="bg-emerald-500 h-full" style={{ width: `${realtimeStatus.progress}%` }}></div>
                </div>
              </div>
              <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                <p className="text-gray-400 text-xs uppercase mb-1">Active Workers</p>
                <p className="text-2xl font-bold text-blue-400">{realtimeStatus.workers}</p>
                <p className="text-[10px] text-gray-500 mt-1">Via IoT Wearables</p>
              </div>
              <div className="bg-white/5 p-4 rounded-lg border border-white/10">
                <p className="text-gray-400 text-xs uppercase mb-1">Material Variance</p>
                <p className="text-2xl font-bold text-amber-400">{realtimeStatus.materialVariance}%</p>
                <p className="text-[10px] text-gray-500 mt-1">As-Built vs As-Planned</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>

      {/* Recent Analyses */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.7 }}
      >
        <Card className="bg-black/40 border-white/10">
          <CardHeader>
            <CardTitle className="text-white flex items-center justify-between">
              <div className="flex items-center">
                <Clock className="mr-2 h-5 w-5" />
                Recent Analyses
              </div>
              <Button variant="outline" size="sm" className="border-white/20 text-white hover:bg-white/10">
                View All
              </Button>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockRecentAnalyses.map((analysis, index) => (
                <motion.div
                  key={analysis.id}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-center justify-between p-4 bg-white/5 rounded-lg border border-white/10 hover:border-white/20 transition-colors"
                >
                  <div className="flex items-center space-x-4">
                    <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-lg flex items-center justify-center">
                      <FileText className="w-5 h-5 text-white" />
                    </div>
                    <div>
                      <h4 className="font-medium text-white">{analysis.name}</h4>
                      <div className="flex items-center space-x-4 text-sm text-gray-400">
                        <span>{analysis.type}</span>
                        <span>•</span>
                        <span>{analysis.size}</span>
                        <span>•</span>
                        <span>{analysis.timestamp}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center space-x-4">
                    {analysis.status === 'completed' && (
                      <Badge variant="secondary" className="bg-green-500/20 text-green-400 border-green-500/30">
                        <CheckCircle className="w-3 h-3 mr-1" />
                        Completed
                      </Badge>
                    )}
                    {analysis.status === 'processing' && (
                      <Badge variant="secondary" className="bg-blue-500/20 text-blue-400 border-blue-500/30">
                        <Clock className="w-3 h-3 mr-1" />
                        Processing
                      </Badge>
                    )}
                    {analysis.status === 'failed' && (
                      <Badge variant="secondary" className="bg-red-500/20 text-red-400 border-red-500/30">
                        <AlertCircle className="w-3 h-3 mr-1" />
                        Failed
                      </Badge>
                    )}
                    <Button variant="ghost" size="sm" className="text-gray-400 hover:text-white">
                      <MoreHorizontal className="w-4 h-4" />
                    </Button>
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

// Analyze page component
const AnalyzePage = () => {
  const [dragActive, setDragActive] = useState(false)
  const [uploadedFiles, setUploadedFiles] = useState([])
  const [analysisSettings, setAnalysisSettings] = useState({
    blueprintType: 'architectural',
    analysisLevel: 'advanced',
    quantumAcceleration: true,
    aiOptimization: true,
    realTimeProcessing: false
  })
  const [realtimeStatus, setRealtimeStatus] = useState({
    siteId: "SITE-001",
    progress: 75.4,
    workers: 24,
    materialVariance: -2.1,
    lastUpdate: new Date().toISOString()
  })
  const fileInputRef = useRef(null)

  const handleDrag = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true)
    } else if (e.type === "dragleave") {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files)
    }
  }, [])

  const handleFiles = (files) => {
    const newFiles = Array.from(files).map(file => ({
      id: Date.now() + Math.random(),
      file,
      name: file.name,
      size: file.size,
      type: file.type,
      status: 'ready'
    }))
    setUploadedFiles(prev => [...prev, ...newFiles])
  }

  const startAnalysis = () => {
    setUploadedFiles(prev => prev.map(file => ({
      ...file,
      status: 'processing',
      progress: 0
    })))

    // Simulate analysis progress
    uploadedFiles.forEach((file, index) => {
      let progress = 0
      const interval = setInterval(() => {
        progress += Math.random() * 15
        if (progress >= 100) {
          progress = 100
          clearInterval(interval)
          setUploadedFiles(prev => prev.map(f => 
            f.id === file.id ? { ...f, status: 'completed', progress: 100 } : f
          ))
        } else {
          setUploadedFiles(prev => prev.map(f => 
            f.id === file.id ? { ...f, progress } : f
          ))
        }
      }, 500)
    })
  }

  return (
    <div className="p-6 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-8"
      >
        <h1 className="text-4xl font-bold text-white mb-4">
          Blueprint <span className="bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">Analysis</span>
        </h1>
        <p className="text-lg text-gray-300 max-w-2xl mx-auto">
          Upload your blueprints and let our AI-powered quantum analysis engine provide detailed insights, 
          material calculations, and optimization recommendations.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upload Section */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-2"
        >
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Upload className="mr-2 h-5 w-5" />
                Upload Blueprints
              </CardTitle>
              <CardDescription>
                Drag and drop your blueprint files or click to browse
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  dragActive 
                    ? 'border-purple-500 bg-purple-500/10' 
                    : 'border-gray-600 hover:border-gray-500'
                }`}
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  multiple
                  accept=".pdf,.dwg,.dxf,.jpg,.jpeg,.png,.bmp,.tiff"
                  onChange={(e) => handleFiles(e.target.files)}
                  className="hidden"
                />
                <motion.div
                  animate={{ scale: dragActive ? 1.1 : 1 }}
                  className="space-y-4"
                >
                  <div className="w-16 h-16 bg-gradient-to-br from-purple-500 to-cyan-500 rounded-full flex items-center justify-center mx-auto">
                    <Upload className="w-8 h-8 text-white" />
                  </div>
                  <div>
                    <p className="text-lg font-medium text-white mb-2">
                      {dragActive ? 'Drop files here' : 'Upload your blueprints'}
                    </p>
                    <p className="text-gray-400 text-sm">
                      Supports PDF, DWG, DXF, JPG, PNG, BMP, TIFF up to 100MB
                    </p>
                  </div>
                  <Button className="bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-600 hover:to-cyan-600">
                    Choose Files
                  </Button>
                </motion.div>
              </div>

              {/* Uploaded Files */}
              {uploadedFiles.length > 0 && (
                <div className="mt-6 space-y-3">
                  <h4 className="font-medium text-white">Uploaded Files</h4>
                  {uploadedFiles.map((file) => (
                    <motion.div
                      key={file.id}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      className="flex items-center justify-between p-3 bg-white/5 rounded-lg border border-white/10"
                    >
                      <div className="flex items-center space-x-3">
                        <div className="w-8 h-8 bg-blue-500/20 rounded flex items-center justify-center">
                          <FileText className="w-4 h-4 text-blue-400" />
                        </div>
                        <div>
                          <p className="text-sm font-medium text-white">{file.name}</p>
                          <p className="text-xs text-gray-400">
                            {(file.size / 1024 / 1024).toFixed(2)} MB
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        {file.status === 'processing' && (
                          <div className="w-24">
                            <Progress value={file.progress || 0} className="h-1" />
                          </div>
                        )}
                        {file.status === 'completed' && (
                          <CheckCircle className="w-5 h-5 text-green-400" />
                        )}
                        {file.status === 'ready' && (
                          <Clock className="w-5 h-5 text-yellow-400" />
                        )}
                        <Button variant="ghost" size="sm" className="text-gray-400 hover:text-white">
                          <Trash2 className="w-4 h-4" />
                        </Button>
                      </div>
                    </motion.div>
                  ))}
                </div>
              )}

              {uploadedFiles.length > 0 && (
                <div className="mt-6 flex justify-center">
                  <Button 
                    onClick={startAnalysis}
                    size="lg"
                    className="bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-600 hover:to-cyan-600"
                    disabled={uploadedFiles.some(f => f.status === 'processing')}
                  >
                    <Zap className="mr-2 h-5 w-5" />
                    {uploadedFiles.some(f => f.status === 'processing') ? 'Analyzing...' : 'Start Analysis'}
                  </Button>
                </div>
              )}
            </CardContent>
          </Card>
        </motion.div>

        {/* Settings Panel */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Settings className="mr-2 h-5 w-5" />
                Analysis Settings
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label className="text-white">Blueprint Type</Label>
                <Select 
                  value={analysisSettings.blueprintType} 
                  onValueChange={(value) => setAnalysisSettings(prev => ({ ...prev, blueprintType: value }))}
                >
                  <SelectTrigger className="bg-white/5 border-white/10 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="architectural">Architectural</SelectItem>
                    <SelectItem value="structural">Structural</SelectItem>
                    <SelectItem value="electrical">Electrical</SelectItem>
                    <SelectItem value="mechanical">Mechanical</SelectItem>
                    <SelectItem value="plumbing">Plumbing</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label className="text-white">Analysis Level</Label>
                <Select 
                  value={analysisSettings.analysisLevel} 
                  onValueChange={(value) => setAnalysisSettings(prev => ({ ...prev, analysisLevel: value }))}
                >
                  <SelectTrigger className="bg-white/5 border-white/10 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="basic">Basic</SelectItem>
                    <SelectItem value="standard">Standard</SelectItem>
                    <SelectItem value="advanced">Advanced</SelectItem>
                    <SelectItem value="comprehensive">Comprehensive</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <Separator className="bg-white/10" />

              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <div className="space-y-1">
                    <Label className="text-white flex items-center">
                      <Atom className="mr-2 h-4 w-4 text-purple-400" />
                      Quantum Acceleration
                    </Label>
                    <p className="text-xs text-gray-400">Use quantum computing for faster processing</p>
                  </div>
                  <Switch 
                    checked={analysisSettings.quantumAcceleration}
                    onCheckedChange={(checked) => setAnalysisSettings(prev => ({ ...prev, quantumAcceleration: checked }))}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-1">
                    <Label className="text-white flex items-center">
                      <Brain className="mr-2 h-4 w-4 text-cyan-400" />
                      AI Optimization
                    </Label>
                    <p className="text-xs text-gray-400">Enhanced AI-powered analysis</p>
                  </div>
                  <Switch 
                    checked={analysisSettings.aiOptimization}
                    onCheckedChange={(checked) => setAnalysisSettings(prev => ({ ...prev, aiOptimization: checked }))}
                  />
                </div>

                <div className="flex items-center justify-between">
                  <div className="space-y-1">
                    <Label className="text-white flex items-center">
                      <Activity className="mr-2 h-4 w-4 text-green-400" />
                      Real-time Processing
                    </Label>
                    <p className="text-xs text-gray-400">Process files as they upload</p>
                  </div>
                  <Switch 
                    checked={analysisSettings.realTimeProcessing}
                    onCheckedChange={(checked) => setAnalysisSettings(prev => ({ ...prev, realTimeProcessing: checked }))}
                  />
                </div>
              </div>

              <Separator className="bg-white/10" />

              <div className="p-4 bg-gradient-to-r from-purple-500/10 to-cyan-500/10 rounded-lg border border-purple-500/20">
                <div className="flex items-center space-x-2 mb-2">
                  <Sparkles className="w-4 h-4 text-yellow-400" />
                  <span className="text-sm font-medium text-white">Estimated Processing</span>
                </div>
                <p className="text-2xl font-bold text-white">~3.2s</p>
                <p className="text-xs text-gray-400">Per blueprint with quantum acceleration</p>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}

// Quantum Lab page component
const QuantumLab = () => {
  const [quantumState, setQuantumState] = useState('superposition')
  const [qubitCount, setQubitCount] = useState([16])
  const [coherenceTime, setCoherenceTime] = useState(94.7)
  const [isRunning, setIsRunning] = useState(false)

  const quantumOperations = [
    { name: 'Hadamard Gate', symbol: 'H', description: 'Creates superposition', complexity: 'Low' },
    { name: 'CNOT Gate', symbol: 'CNOT', description: 'Quantum entanglement', complexity: 'Medium' },
    { name: 'Toffoli Gate', symbol: 'CCX', description: 'Quantum AND operation', complexity: 'High' },
    { name: 'Quantum Fourier Transform', symbol: 'QFT', description: 'Frequency analysis', complexity: 'Very High' }
  ]

  return (
    <div className="p-6 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-8"
      >
        <h1 className="text-4xl font-bold text-white mb-4">
          Quantum <span className="bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">Laboratory</span>
        </h1>
        <p className="text-lg text-gray-300 max-w-2xl mx-auto">
          Advanced quantum computing interface for blueprint optimization and complex architectural calculations.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Quantum Circuit Visualizer */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-2"
        >
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Atom className="mr-2 h-5 w-5" />
                Quantum Circuit Designer
              </CardTitle>
              <CardDescription>
                Design and simulate quantum circuits for blueprint analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="bg-black/60 rounded-lg p-6 mb-6">
                <div className="grid grid-cols-4 gap-4 mb-4">
                  {[...Array(qubitCount[0])].map((_, i) => (
                    <div key={i} className="flex items-center space-x-2">
                      <span className="text-white text-sm">|q{i}⟩</span>
                      <div className="flex-1 h-1 bg-gradient-to-r from-purple-500 to-cyan-500 rounded"></div>
                    </div>
                  ))}
                </div>
                <div className="text-center">
                  <motion.div
                    animate={{ rotate: isRunning ? 360 : 0 }}
                    transition={{ duration: 2, repeat: isRunning ? Infinity : 0, ease: "linear" }}
                    className="inline-block"
                  >
                    <Atom className="w-12 h-12 text-purple-400" />
                  </motion.div>
                  <p className="text-white mt-2">Quantum State: {quantumState}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {quantumOperations.map((op, index) => (
                  <motion.div
                    key={op.name}
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    className="p-4 bg-gradient-to-br from-purple-500/20 to-cyan-500/20 rounded-lg border border-purple-500/30 cursor-pointer hover:border-purple-400/50 transition-colors"
                  >
                    <div className="text-center">
                      <div className="w-12 h-12 bg-purple-500/30 rounded-lg flex items-center justify-center mx-auto mb-2">
                        <span className="text-white font-mono text-xs">{op.symbol}</span>
                      </div>
                      <h4 className="text-white text-sm font-medium">{op.name}</h4>
                      <p className="text-gray-400 text-xs mt-1">{op.description}</p>
                      <Badge variant="outline" className="mt-2 text-xs">
                        {op.complexity}
                      </Badge>
                    </div>
                  </motion.div>
                ))}
              </div>

              <div className="mt-6 flex justify-center space-x-4">
                <Button 
                  onClick={() => setIsRunning(!isRunning)}
                  className="bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-600 hover:to-cyan-600"
                >
                  {isRunning ? <Pause className="mr-2 h-4 w-4" /> : <Play className="mr-2 h-4 w-4" />}
                  {isRunning ? 'Pause' : 'Run'} Circuit
                </Button>
                <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
                  <RotateCcw className="mr-2 h-4 w-4" />
                  Reset
                </Button>
                <Button variant="outline" className="border-white/20 text-white hover:bg-white/10">
                  <Save className="mr-2 h-4 w-4" />
                  Save Circuit
                </Button>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* Quantum Controls */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="space-y-6"
        >
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Settings className="mr-2 h-5 w-5" />
                Quantum Parameters
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label className="text-white">Qubit Count: {qubitCount[0]}</Label>
                <Slider
                  value={qubitCount}
                  onValueChange={setQubitCount}
                  max={32}
                  min={4}
                  step={2}
                  className="w-full"
                />
                <p className="text-xs text-gray-400">Higher qubit count increases computational power</p>
              </div>

              <div className="space-y-2">
                <Label className="text-white">Coherence Time</Label>
                <div className="flex items-center space-x-2">
                  <Progress value={coherenceTime} className="flex-1" />
                  <span className="text-white text-sm">{coherenceTime.toFixed(1)}%</span>
                </div>
                <p className="text-xs text-gray-400">Quantum state stability measure</p>
              </div>

              <Separator className="bg-white/10" />

              <div className="space-y-4">
                <h4 className="text-white font-medium">Quantum State</h4>
                <div className="space-y-2">
                  {['superposition', 'entangled', 'measured'].map((state) => (
                    <div key={state} className="flex items-center space-x-2">
                      <input
                        type="radio"
                        id={state}
                        name="quantumState"
                        checked={quantumState === state}
                        onChange={() => setQuantumState(state)}
                        className="text-purple-500"
                      />
                      <Label htmlFor={state} className="text-white capitalize">
                        {state}
                      </Label>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Activity className="mr-2 h-5 w-5" />
                System Status
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Quantum Processor</span>
                <Badge className="bg-green-500/20 text-green-400 border-green-500/30">
                  Online
                </Badge>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Error Rate</span>
                <span className="text-white">0.001%</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Temperature</span>
                <span className="text-white">15 mK</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-300">Fidelity</span>
                <span className="text-white">99.7%</span>
              </div>
            </CardContent>
          </Card>
        </motion.div>
      </div>

      {/* Quantum Algorithms */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <Card className="bg-black/40 border-white/10">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Brain className="mr-2 h-5 w-5" />
              Quantum Algorithms
            </CardTitle>
            <CardDescription>
              Pre-built quantum algorithms optimized for blueprint analysis
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {[
                {
                  name: 'Grover\'s Search',
                  description: 'Optimal database search for blueprint elements',
                  complexity: 'O(√N)',
                  speedup: '1000x'
                },
                {
                  name: 'Shor\'s Algorithm',
                  description: 'Factorization for structural analysis',
                  complexity: 'O(log³N)',
                  speedup: 'Exponential'
                },
                {
                  name: 'VQE Optimizer',
                  description: 'Variational quantum eigensolver for materials',
                  complexity: 'O(N⁴)',
                  speedup: '500x'
                },
                {
                  name: 'QAOA',
                  description: 'Quantum approximate optimization',
                  complexity: 'O(N²)',
                  speedup: '200x'
                },
                {
                  name: 'HHL Solver',
                  description: 'Linear systems for structural equations',
                  complexity: 'O(log N)',
                  speedup: 'Exponential'
                },
                {
                  name: 'Quantum ML',
                  description: 'Machine learning acceleration',
                  complexity: 'O(log MN)',
                  speedup: '10000x'
                }
              ].map((algorithm, index) => (
                <motion.div
                  key={algorithm.name}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="p-4 bg-gradient-to-br from-purple-500/10 to-cyan-500/10 rounded-lg border border-purple-500/20 hover:border-purple-400/40 transition-colors cursor-pointer"
                >
                  <h4 className="text-white font-medium mb-2">{algorithm.name}</h4>
                  <p className="text-gray-400 text-sm mb-3">{algorithm.description}</p>
                  <div className="flex justify-between items-center text-xs">
                    <span className="text-purple-400">Complexity: {algorithm.complexity}</span>
                    <Badge variant="outline" className="text-cyan-400 border-cyan-400/30">
                      {algorithm.speedup}
                    </Badge>
                  </div>
                </motion.div>
              ))}
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  )
}

// AI Studio page component
const AIStudio = () => {
  const [selectedModel, setSelectedModel] = useState('gpt-4-turbo')
  const [prompt, setPrompt] = useState('')
  const [response, setResponse] = useState('')
  const [isGenerating, setIsGenerating] = useState(false)

  const aiModels = [
    { id: 'gpt-4-turbo', name: 'GPT-4 Turbo', provider: 'OpenAI', capability: 'General AI' },
    { id: 'claude-3', name: 'Claude 3', provider: 'Anthropic', capability: 'Reasoning' },
    { id: 'gemini-pro', name: 'Gemini Pro', provider: 'Google', capability: 'Multimodal' },
    { id: 'llama-2', name: 'Llama 2', provider: 'Meta', capability: 'Open Source' }
  ]

  const generateResponse = async () => {
    setIsGenerating(true)
    setResponse('')
    
    // Simulate AI response generation
    const words = [
      'Analyzing', 'blueprint', 'structure', 'optimization', 'efficiency', 'materials',
      'calculations', 'recommendations', 'safety', 'compliance', 'standards', 'design',
      'architectural', 'engineering', 'quantum', 'enhanced', 'processing', 'algorithms'
    ]
    
    let currentResponse = ''
    for (let i = 0; i < 50; i++) {
      await new Promise(resolve => setTimeout(resolve, 100))
      const word = words[Math.floor(Math.random() * words.length)]
      currentResponse += word + ' '
      setResponse(currentResponse)
    }
    
    setIsGenerating(false)
  }

  return (
    <div className="p-6 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-8"
      >
        <h1 className="text-4xl font-bold text-white mb-4">
          AI <span className="bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">Studio</span>
        </h1>
        <p className="text-lg text-gray-300 max-w-2xl mx-auto">
          Interact with advanced AI models to generate insights, analyze blueprints, and optimize designs.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* AI Chat Interface */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="lg:col-span-3"
        >
          <Card className="bg-black/40 border-white/10 h-[600px] flex flex-col">
            <CardHeader>
              <CardTitle className="text-white flex items-center justify-between">
                <div className="flex items-center">
                  <Brain className="mr-2 h-5 w-5" />
                  AI Assistant
                </div>
                <Badge className="bg-green-500/20 text-green-400 border-green-500/30">
                  {selectedModel}
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 flex flex-col">
              <ScrollArea className="flex-1 mb-4 p-4 bg-black/60 rounded-lg">
                <div className="space-y-4">
                  <div className="flex items-start space-x-3">
                    <Avatar className="w-8 h-8">
                      <AvatarFallback className="bg-purple-500">AI</AvatarFallback>
                    </Avatar>
                    <div className="flex-1 bg-white/5 rounded-lg p-3">
                      <p className="text-white text-sm">
                        Hello! I'm your AI assistant specialized in blueprint analysis and architectural optimization. 
                        How can I help you today?
                      </p>
                    </div>
                  </div>
                  
                  {response && (
                    <div className="flex items-start space-x-3">
                      <Avatar className="w-8 h-8">
                        <AvatarFallback className="bg-purple-500">AI</AvatarFallback>
                      </Avatar>
                      <div className="flex-1 bg-white/5 rounded-lg p-3">
                        <p className="text-white text-sm">
                          {response}
                          {isGenerating && <span className="animate-pulse">|</span>}
                        </p>
                      </div>
                    </div>
                  )}
                </div>
              </ScrollArea>
              
              <div className="space-y-3">
                <Textarea
                  placeholder="Ask me anything about blueprint analysis, structural optimization, or architectural design..."
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  className="bg-white/5 border-white/10 text-white placeholder-gray-400 min-h-[100px]"
                />
                <div className="flex justify-between items-center">
                  <div className="flex space-x-2">
                    <Button variant="outline" size="sm" className="border-white/20 text-white hover:bg-white/10">
                      <Mic className="w-4 h-4" />
                    </Button>
                    <Button variant="outline" size="sm" className="border-white/20 text-white hover:bg-white/10">
                      <Image className="w-4 h-4" />
                    </Button>
                    <Button variant="outline" size="sm" className="border-white/20 text-white hover:bg-white/10">
                      <FileText className="w-4 h-4" />
                    </Button>
                  </div>
                  <Button 
                    onClick={generateResponse}
                    disabled={!prompt.trim() || isGenerating}
                    className="bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-600 hover:to-cyan-600"
                  >
                    {isGenerating ? (
                      <RefreshCw className="mr-2 h-4 w-4 animate-spin" />
                    ) : (
                      <Send className="mr-2 h-4 w-4" />
                    )}
                    {isGenerating ? 'Generating...' : 'Send'}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </motion.div>

        {/* AI Model Selection & Settings */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="space-y-6"
        >
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Cpu className="mr-2 h-5 w-5" />
                AI Models
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              {aiModels.map((model) => (
                <motion.div
                  key={model.id}
                  whileHover={{ scale: 1.02 }}
                  className={`p-3 rounded-lg border cursor-pointer transition-colors ${
                    selectedModel === model.id
                      ? 'border-purple-500/50 bg-purple-500/10'
                      : 'border-white/10 hover:border-white/20'
                  }`}
                  onClick={() => setSelectedModel(model.id)}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="text-white font-medium">{model.name}</h4>
                    {selectedModel === model.id && (
                      <CheckCircle className="w-4 h-4 text-purple-400" />
                    )}
                  </div>
                  <p className="text-xs text-gray-400">{model.provider}</p>
                  <Badge variant="outline" className="mt-2 text-xs">
                    {model.capability}
                  </Badge>
                </motion.div>
              ))}
            </CardContent>
          </Card>

          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Settings className="mr-2 h-5 w-5" />
                Generation Settings
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label className="text-white">Temperature</Label>
                <Slider defaultValue={[0.7]} max={1} min={0} step={0.1} />
                <p className="text-xs text-gray-400">Controls creativity vs accuracy</p>
              </div>
              
              <div className="space-y-2">
                <Label className="text-white">Max Tokens</Label>
                <Slider defaultValue={[1000]} max={4000} min={100} step={100} />
                <p className="text-xs text-gray-400">Maximum response length</p>
              </div>

              <div className="space-y-2">
                <Label className="text-white">Top P</Label>
                <Slider defaultValue={[0.9]} max={1} min={0} step={0.1} />
                <p className="text-xs text-gray-400">Nucleus sampling threshold</p>
              </div>
            </CardContent>
          </Card>

          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Lightbulb className="mr-2 h-5 w-5" />
                Quick Prompts
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {[
                'Analyze this blueprint for structural integrity',
                'Optimize material usage for cost efficiency',
                'Generate compliance report for building codes',
                'Suggest design improvements for energy efficiency',
                'Calculate load-bearing requirements'
              ].map((quickPrompt, index) => (
                <Button
                  key={index}
                  variant="ghost"
                  size="sm"
                  className="w-full text-left justify-start text-gray-300 hover:text-white hover:bg-white/5"
                  onClick={() => setPrompt(quickPrompt)}
                >
                  <ChevronRight className="w-3 h-3 mr-2" />
                  {quickPrompt}
                </Button>
              ))}
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}

// Projects page component
const ProjectsPage = () => {
  const [projects] = useState([
    {
      id: 1,
      name: 'Downtown Office Complex',
      type: 'Commercial',
      status: 'In Progress',
      progress: 75,
      lastModified: '2 hours ago',
      blueprints: 12,
      team: 4
    },
    {
      id: 2,
      name: 'Residential Tower A',
      type: 'Residential',
      status: 'Completed',
      progress: 100,
      lastModified: '1 day ago',
      blueprints: 8,
      team: 3
    },
    {
      id: 3,
      name: 'Shopping Mall Extension',
      type: 'Retail',
      status: 'Planning',
      progress: 25,
      lastModified: '3 days ago',
      blueprints: 5,
      team: 6
    }
  ])

  return (
    <div className="p-6 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex justify-between items-center"
      >
        <div>
          <h1 className="text-4xl font-bold text-white mb-2">Projects</h1>
          <p className="text-gray-300">Manage your blueprint analysis projects</p>
        </div>
        <Button className="bg-gradient-to-r from-purple-500 to-cyan-500 hover:from-purple-600 hover:to-cyan-600">
          <Plus className="mr-2 h-4 w-4" />
          New Project
        </Button>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map((project, index) => (
          <motion.div
            key={project.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <Card className="bg-black/40 border-white/10 hover:border-white/20 transition-colors cursor-pointer">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-white">{project.name}</CardTitle>
                    <CardDescription>{project.type}</CardDescription>
                  </div>
                  <Badge 
                    variant="outline" 
                    className={
                      project.status === 'Completed' ? 'border-green-500/30 text-green-400' :
                      project.status === 'In Progress' ? 'border-blue-500/30 text-blue-400' :
                      'border-yellow-500/30 text-yellow-400'
                    }
                  >
                    {project.status}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-400">Progress</span>
                    <span className="text-white">{project.progress}%</span>
                  </div>
                  <Progress value={project.progress} className="h-2" />
                </div>
                
                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div className="flex items-center space-x-2">
                    <FileText className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-400">{project.blueprints} blueprints</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <Users className="w-4 h-4 text-gray-400" />
                    <span className="text-gray-400">{project.team} members</span>
                  </div>
                </div>
                
                <div className="flex justify-between items-center pt-2 border-t border-white/10">
                  <span className="text-xs text-gray-400">Modified {project.lastModified}</span>
                  <div className="flex space-x-1">
                    <Button variant="ghost" size="sm" className="text-gray-400 hover:text-white">
                      <Eye className="w-4 h-4" />
                    </Button>
                    <Button variant="ghost" size="sm" className="text-gray-400 hover:text-white">
                      <Edit3 className="w-4 h-4" />
                    </Button>
                    <Button variant="ghost" size="sm" className="text-gray-400 hover:text-white">
                      <Share2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </div>
    </div>
  )
}

// Analytics page component
const AnalyticsPage = () => {
  return (
    <div className="p-6 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-8"
      >
        <h1 className="text-4xl font-bold text-white mb-4">
          Advanced <span className="bg-gradient-to-r from-purple-400 to-cyan-400 bg-clip-text text-transparent">Analytics</span>
        </h1>
        <p className="text-lg text-gray-300 max-w-2xl mx-auto">
          Deep insights into your blueprint analysis performance, trends, and optimization opportunities.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white">Performance Trends</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={mockAnalysisData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                  <XAxis dataKey="name" stroke="#9CA3AF" />
                  <YAxis stroke="#9CA3AF" />
                  <RechartsTooltip 
                    contentStyle={{ 
                      backgroundColor: '#1F2937', 
                      border: '1px solid #374151',
                      borderRadius: '8px'
                    }}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="efficiency" 
                    stackId="1"
                    stroke="#8B5CF6" 
                    fill="#8B5CF6" 
                    fillOpacity={0.3}
                  />
                  <Area 
                    type="monotone" 
                    dataKey="accuracy" 
                    stackId="2"
                    stroke="#06B6D4" 
                    fill="#06B6D4" 
                    fillOpacity={0.3}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
        >
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white">Blueprint Distribution</CardTitle>
            </CardHeader>
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <RechartsPieChart>
                  <RechartsTooltip 
                    contentStyle={{ 
                      backgroundColor: '#1F2937', 
                      border: '1px solid #374151',
                      borderRadius: '8px'
                    }}
                  />
                  <RechartsPie
                    data={mockBlueprintTypes}
                    cx="50%"
                    cy="50%"
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="count"
                    label={({ name, percentage }) => `${name} ${percentage}%`}
                  >
                    {mockBlueprintTypes.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={['#8B5CF6', '#06B6D4', '#10B981', '#F59E0B'][index]} />
                    ))}
                  </RechartsPie>
                </RechartsPieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </motion.div>
      </div>
    </div>
  )
}

// Settings page component
const SettingsPage = () => {
  return (
    <div className="p-6 space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-4xl font-bold text-white mb-2">Settings</h1>
        <p className="text-gray-300">Configure your ArciTEK.AI experience</p>
      </motion.div>

      <Tabs defaultValue="general" className="space-y-6">
        <TabsList className="bg-black/40 border border-white/10">
          <TabsTrigger value="general" className="text-white">General</TabsTrigger>
          <TabsTrigger value="ai" className="text-white">AI & Quantum</TabsTrigger>
          <TabsTrigger value="notifications" className="text-white">Notifications</TabsTrigger>
          <TabsTrigger value="security" className="text-white">Security</TabsTrigger>
        </TabsList>

        <TabsContent value="general">
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white">General Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="space-y-2">
                <Label className="text-white">Theme</Label>
                <Select defaultValue="dark">
                  <SelectTrigger className="bg-white/5 border-white/10 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="dark">Dark</SelectItem>
                    <SelectItem value="light">Light</SelectItem>
                    <SelectItem value="auto">Auto</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <div className="space-y-2">
                <Label className="text-white">Language</Label>
                <Select defaultValue="en">
                  <SelectTrigger className="bg-white/5 border-white/10 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="en">English</SelectItem>
                    <SelectItem value="es">Spanish</SelectItem>
                    <SelectItem value="fr">French</SelectItem>
                    <SelectItem value="de">German</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="ai">
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white">AI & Quantum Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-white">Enable Quantum Acceleration</Label>
                  <p className="text-sm text-gray-400">Use quantum computing for faster processing</p>
                </div>
                <Switch defaultChecked />
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-white">AI Auto-optimization</Label>
                  <p className="text-sm text-gray-400">Automatically optimize analysis parameters</p>
                </div>
                <Switch defaultChecked />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="notifications">
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white">Notification Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-white">Analysis Complete</Label>
                  <p className="text-sm text-gray-400">Notify when blueprint analysis is finished</p>
                </div>
                <Switch defaultChecked />
              </div>
              
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-white">System Updates</Label>
                  <p className="text-sm text-gray-400">Receive notifications about system updates</p>
                </div>
                <Switch />
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="security">
          <Card className="bg-black/40 border-white/10">
            <CardHeader>
              <CardTitle className="text-white">Security Settings</CardTitle>
            </CardHeader>
            <CardContent className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <Label className="text-white">Two-Factor Authentication</Label>
                  <p className="text-sm text-gray-400">Add an extra layer of security</p>
                </div>
                <Switch />
              </div>
              
              <div className="space-y-2">
                <Label className="text-white">Session Timeout</Label>
                <Select defaultValue="30">
                  <SelectTrigger className="bg-white/5 border-white/10 text-white">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="15">15 minutes</SelectItem>
                    <SelectItem value="30">30 minutes</SelectItem>
                    <SelectItem value="60">1 hour</SelectItem>
                    <SelectItem value="never">Never</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

// Main App component
function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <TooltipProvider>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white">
          <AnimatedBackground />
          
          <div className="flex h-screen">
            <Navigation isOpen={sidebarOpen} setIsOpen={setSidebarOpen} />
            
            <div className="flex-1 flex flex-col overflow-hidden">
              <Header setIsOpen={setSidebarOpen} />
              
              <main className="flex-1 overflow-y-auto">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/analyze" element={<AnalyzePage />} />
                  <Route path="/quantum" element={<QuantumLab />} />
                  <Route path="/ai-studio" element={<AIStudio />} />
                  <Route path="/projects" element={<ProjectsPage />} />
                  <Route path="/analytics" element={<AnalyticsPage />} />
                  <Route path="/settings" element={<SettingsPage />} />
                </Routes>
              </main>
            </div>
          </div>
        </div>
      </Router>
    </TooltipProvider>
  )
}

export default App

