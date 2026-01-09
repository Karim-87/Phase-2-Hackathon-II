export interface UserSession {
  jwt_token: string;
  user_id: string;
  expires_at: string;
  is_authenticated: boolean;
}