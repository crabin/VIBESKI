// ===================================================================
// 通用类型定义
// ===================================================================

// -- Chat --
export interface ChatRequest {
  message: string;
  agent?: string;
  prompt?: string;
}

export interface ChatResponse {
  response: string;
  agent: string;
}

export interface SSEEvent {
  event: string;
  data: Record<string, any>;
}

export type RootAction = 'run_once' | 'always_allow' | 'deny';

// -- ReAct 渲染块 --
// 每个块对应 CLI TUI 中的一个视觉面板

export type BlockType =
  | 'user'           // 用户消息
  | 'planning'       // 📋 规划面板
  | 'task_phase'     // 状态指示器（spinner）
  | 'thinking'       // 💭 推理面板（流式）
  | 'execution'      // ⚡ 执行面板
  | 'exec_result'    // 执行结果（成功/失败）
  | 'observation'    // 观察/内容
  | 'report'         // 📊 报告面板（流式）
  | 'response'       // 最终完整响应
  | 'error';         // 错误

export interface RenderBlock {
  id: string;
  type: BlockType;
  timestamp: Date;
  // 各类型的数据载荷
  content?: string;
  // 事件来源的智能体
  agent?: string;
  // thinking
  iteration?: number;
  streaming?: boolean;
  // execution
  tool?: string;
  params?: Record<string, any>;
  // exec_result
  success?: boolean;
  result?: any;
  error?: string;
  // task_phase
  phase?: 'planning' | 'thinking' | 'exec' | 'report' | 'done';
  detail?: string;
}

// -- Agents --
export interface AgentInfo {
  type: string;
  name: string;
  description: string;
}

export interface AgentListResponse {
  agents: AgentInfo[];
}

// -- System --
export interface SystemInfoResponse {
  platform: string;
  python_version: string;
  database_url: string;
  config_source: string;
}

export interface SystemStatusResponse {
  status: 'ok' | 'error';
  version: string;
  message?: string;
}

// -- Database --
export interface DbStatsResponse {
  conversations: number;
  prompt_chains: number;
  user_configs: number;
}

export interface ConversationRecord {
  timestamp: string;
  agent_type: string;
  user_message: string;
  assistant_message: string;
}

export interface DbHistoryResponse {
  conversations: ConversationRecord[];
}

export interface DbClearResponse {
  success: boolean;
  deleted_count: number;
  message: string;
}

// -- 通用 --
export interface ApiError {
  detail: string;
}

// -- 旧消息类型（保留兼容） --
export interface Message {
  id: string;
  role: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  eventType?: string;
}
