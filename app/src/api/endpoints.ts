// ===================================================================
// API 端点调用方法
// ===================================================================

import api from './client';
import type {
  ChatRequest,
  ChatResponse,
  AgentListResponse,
  RootAction,
  SystemInfoResponse,
  SystemStatusResponse,
  DbStatsResponse,
} from './types';

// -- Chat --
export const sendMessage = (data: ChatRequest) =>
  api.post<ChatResponse>('/api/chat', data);

export const sendMessageStream = (data: ChatRequest) =>
  // Use fetch with streaming enabled
  return fetch(`${api.defaults.baseURL}/api/chat/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });

// -- Agents --
export const getAgents = () =>
  api.get<AgentListResponse>('/api/agents');

export const setRootAction = (action: RootAction) =>
  api.post('/api/root-action', { action });

// -- System --
export const getSystemInfo = () =>
  api.get<SystemInfoResponse>('/api/system/info');

export const getSystemStatus = () =>
  api.get<SystemStatusResponse>('/api/system/status');

// -- Database --
export const getDbStats = () =>
  api.get<DbStatsResponse>('/api/db/stats');

export const getDbHistory = (params?: {
  agent?: string;
  limit?: number;
  session_id?: string;
}) => {
  const search = new URLSearchParams();
  if (params?.agent) search.set('agent', params.agent);
  if (params?.limit) search.set('limit', String(params.limit));
  if (params?.session_id) search.set('session_id', params.session_id);
  const qs = search.toString();
  return api.get<DbHistoryResponse>(`/api/db/history${qs ? `?${qs}` : ''}`);
};

export const clearDbHistory = (params?: {
  agent?: string;
  session_id?: string;
}) => {
  const search = new URLSearchParams();
  if (params?.agent) search.set('agent', params.agent);
  if (params?.session_id) search.set('session_id', params.session_id);
  const qs = search.toString();
  return api.delete<DbClearResponse>(`/api/db/history${qs ? `?${qs}` : ''}`);
};
