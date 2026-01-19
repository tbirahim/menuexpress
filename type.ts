
export interface MenuItem {
  id: string;
  name: string;
  price: number;
  description: string;
  image: string;
  category: string;
}

export interface CartItem extends MenuItem {
  quantity: number;
}

export interface Order {
  id: string;
  items: CartItem[];
  total: number;
  type: 'Sur place' | 'Livraison';
  logistics: string;
  timestamp: number;
}

export type View = 'home' | 'menu' | 'reserve' | 'cart' | 'admin';
