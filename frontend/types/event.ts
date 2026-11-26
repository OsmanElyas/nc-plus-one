export interface Event {
  id: number;
  title: string;
  starts_at: string;
  ends_at: string;
  location: string;
}

export interface EventDetail extends Event {
  description: string | null;
  address: string | null;
  capacity: number | null;
  created_at: string;
  organiser: {
    id: number;
    name: string;
  } | null;
}