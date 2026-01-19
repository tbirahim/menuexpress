
import React, { useState, useEffect, useMemo } from 'react';
import { View, MenuItem, CartItem, Order } from './types';
import { INITIAL_MENU, WHATSAPP_NUMBER, CALL_NUMBER, ADMIN_PASS } from './constants';
import { getChefRecommendation } from './services/geminiService';

// --- Helper Components ---

const Navbar: React.FC<{ 
  currentView: View, 
  setView: (v: View) => void, 
  cartCount: number 
}> = ({ currentView, setView, cartCount }) => (
  <nav className="fixed bottom-0 left-0 right-0 z-50 bg-zinc-900 border-t border-amber-500/30 md:top-0 md:bottom-auto md:border-b md:border-t-0 p-2 md:px-8 flex justify-around md:justify-between items-center backdrop-blur-md bg-opacity-90">
    <div className="hidden md:block">
      <h1 className="text-xl text-amber-500 font-bold tracking-widest uppercase">Teranga Express</h1>
    </div>
    <div className="flex gap-4 md:gap-8 overflow-x-auto no-scrollbar">
      <NavItem active={currentView === 'home'} onClick={() => setView('home')} icon="🏠" label="Accueil" />
      <NavItem active={currentView === 'menu'} onClick={() => setView('menu')} icon="🥘" label="La Carte" />
      <NavItem active={currentView === 'reserve'} onClick={() => setView('reserve')} icon="📅" label="Réserver" />
      <NavItem active={currentView === 'cart'} onClick={() => setView('cart')} icon="🛒" label={`Panier (${cartCount})`} />
      <NavItem active={currentView === 'admin'} onClick={() => setView('admin')} icon="⚙️" label="Admin" />
    </div>
    <div className="hidden md:block">
      <a href={`tel:${CALL_NUMBER}`} className="px-4 py-2 border border-amber-500 text-amber-500 rounded-full hover:bg-amber-500 hover:text-black transition-all">
        📞 {CALL_NUMBER}
      </a>
    </div>
  </nav>
);

const NavItem: React.FC<{ active: boolean, onClick: () => void, icon: string, label: string }> = ({ active, onClick, icon, label }) => (
  <button 
    onClick={onClick}
    className={`flex flex-col items-center justify-center p-2 min-w-[60px] transition-colors ${active ? 'text-amber-500' : 'text-zinc-400 hover:text-white'}`}
  >
    <span className="text-xl mb-1">{icon}</span>
    <span className="text-[10px] uppercase font-bold tracking-tighter">{label}</span>
  </button>
);

// --- Main App ---

const App: React.FC = () => {
  const [view, setView] = useState<View>('home');
  const [menu, setMenu] = useState<MenuItem[]>(() => {
    const saved = localStorage.getItem('tg_menu');
    return saved ? JSON.parse(saved) : INITIAL_MENU;
  });
  const [cart, setCart] = useState<CartItem[]>([]);
  const [orders, setOrders] = useState<Order[]>(() => {
    const saved = localStorage.getItem('tg_orders');
    return saved ? JSON.parse(saved) : [];
  });
  const [aiMessage, setAiMessage] = useState("Bonjour ! Je suis le Chef. Besoin d'un conseil ?");
  const [isAiLoading, setIsAiLoading] = useState(false);
  const [adminCode, setAdminCode] = useState("");

  useEffect(() => {
    localStorage.setItem('tg_menu', JSON.stringify(menu));
  }, [menu]);

  useEffect(() => {
    localStorage.setItem('tg_orders', JSON.stringify(orders));
  }, [orders]);

  const addToCart = (item: MenuItem) => {
    setCart(prev => {
      const existing = prev.find(i => i.id === item.id);
      if (existing) {
        return prev.map(i => i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i);
      }
      return [...prev, { ...item, quantity: 1 }];
    });
    alert(`${item.name} ajouté au panier !`);
  };

  const removeFromCart = (id: string) => {
    setCart(prev => prev.filter(i => i.id !== id));
  };

  const cartCount = useMemo(() => cart.reduce((acc, curr) => acc + curr.quantity, 0), [cart]);
  const cartTotal = useMemo(() => cart.reduce((acc, curr) => acc + (curr.price * curr.quantity), 0), [cart]);

  const handleAskChef = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const input = (e.currentTarget.elements.namedItem('aiPrompt') as HTMLInputElement).value;
    if (!input) return;
    
    setIsAiLoading(true);
    const reply = await getChefRecommendation(input, menu);
    setAiMessage(reply);
    setIsAiLoading(false);
    e.currentTarget.reset();
  };

  const handleCheckout = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const formData = new FormData(e.currentTarget);
    const type = formData.get('type') as any;
    const logistics = formData.get('logistics') as string;

    if (!logistics) return alert("Veuillez préciser la table ou l'adresse.");

    const newOrder: Order = {
      id: Math.random().toString(36).substr(2, 9),
      items: [...cart],
      total: cartTotal,
      type,
      logistics,
      timestamp: Date.now(),
    };

    setOrders([newOrder, ...orders]);
    
    const itemString = cart.map(i => `- ${i.name} (x${i.quantity})`).join('\n');
    const msg = `🥘 *NOUVELLE COMMANDE*\n\n${itemString}\n\n💰 Total: ${cartTotal} FCFA\n📍 Mode: ${type}\n📝 Détails: ${logistics}`;
    const waLink = `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`;
    
    window.open(waLink, '_blank');
    setCart([]);
    setView('home');
    alert("Commande envoyée ! Redirection vers WhatsApp...");
  };

  return (
    <div className="min-h-screen pb-24 md:pt-20 bg-zinc-950 text-zinc-100 flex flex-col">
      <Navbar currentView={view} setView={setView} cartCount={cartCount} />

      <main className="flex-1 container mx-auto px-4 max-w-6xl py-8">
        
        {/* VIEW: HOME */}
        {view === 'home' && (
          <div className="space-y-12 animate-in fade-in duration-700">
            <div className="relative rounded-3xl overflow-hidden h-[400px] flex items-center justify-center">
              <img 
                src="https://www.luxe-infinity-afrique.com/wp-content/uploads/2025/08/La-Cuisine-Africaine-Conquiert-la-France-1200x675.webp" 
                className="absolute inset-0 w-full h-full object-cover opacity-60"
                alt="Banner"
              />
              <div className="relative z-10 text-center space-y-4 px-4">
                <h1 className="text-5xl md:text-7xl font-serif text-amber-500">Teranga Gourmet</h1>
                <p className="text-xl md:text-2xl font-light italic text-zinc-200">L'Authenticité du Sénégal dans votre assiette</p>
                <button 
                  onClick={() => setView('menu')}
                  className="px-8 py-3 bg-amber-500 text-black font-bold rounded-full hover:bg-amber-400 transition-all shadow-lg"
                >
                  Découvrir la Carte
                </button>
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-8 items-center bg-zinc-900/50 p-8 rounded-3xl border border-zinc-800">
              <div className="space-y-4">
                <h2 className="text-3xl text-amber-500">Le Conseil du Chef (AI)</h2>
                <div className="bg-zinc-800 p-4 rounded-xl border-l-4 border-amber-500 min-h-[100px] flex items-center">
                  <p className={isAiLoading ? 'animate-pulse text-amber-500/50' : ''}>
                    {isAiLoading ? "Le chef réfléchit..." : aiMessage}
                  </p>
                </div>
                <form onSubmit={handleAskChef} className="flex gap-2">
                  <input 
                    name="aiPrompt"
                    placeholder="Qu'est-ce qui est bon aujourd'hui ?" 
                    className="flex-1 bg-zinc-900 border border-zinc-700 rounded-lg px-4 py-2 focus:outline-none focus:border-amber-500"
                  />
                  <button type="submit" className="bg-amber-500 text-black px-6 py-2 rounded-lg font-bold">Demander</button>
                </form>
              </div>
              <img 
                src="https://images.unsplash.com/photo-1556910103-1c02745aae4d?q=80&w=800" 
                className="rounded-2xl h-64 w-full object-cover"
                alt="Chef"
              />
            </div>
          </div>
        )}

        {/* VIEW: MENU */}
        {view === 'menu' && (
          <div className="space-y-8 animate-in slide-in-from-bottom duration-500">
            <div className="text-center">
              <h1 className="text-4xl text-amber-500 mb-2">Notre Menu Gourmet</h1>
              <p className="text-zinc-400">Des produits frais, des épices authentiques</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {menu.map(item => (
                <div key={item.id} className="bg-zinc-900 rounded-2xl overflow-hidden border border-zinc-800 hover:border-amber-500/50 transition-all group">
                  <div className="relative h-48">
                    <img src={item.image} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500" alt={item.name} />
                    <div className="absolute top-2 right-2 bg-black/70 px-3 py-1 rounded-full text-amber-500 font-bold text-sm">
                      {item.price} F
                    </div>
                  </div>
                  <div className="p-5 space-y-3">
                    <h3 className="text-xl font-bold">{item.name}</h3>
                    <p className="text-zinc-400 text-sm line-clamp-2">{item.description}</p>
                    <button 
                      onClick={() => addToCart(item)}
                      className="w-full py-2 border-2 border-amber-500/30 text-amber-500 rounded-xl hover:bg-amber-500 hover:text-black font-bold transition-all"
                    >
                      Ajouter au Panier
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* VIEW: RESERVE */}
        {view === 'reserve' && (
          <div className="max-w-2xl mx-auto space-y-8 animate-in zoom-in duration-300">
             <div className="relative rounded-2xl overflow-hidden h-48 mb-8">
              <img src="https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?q=80&w=800" className="w-full h-full object-cover opacity-50" alt="Res" />
              <div className="absolute inset-0 flex items-center justify-center">
                <h1 className="text-4xl text-amber-500">Réserver une Table</h1>
              </div>
            </div>
            
            <form className="bg-zinc-900 p-8 rounded-3xl border border-zinc-800 space-y-6" onSubmit={(e) => {
              e.preventDefault();
              const d = new FormData(e.currentTarget);
              const msg = `📝 *RÉSERVATION*\n\n👤 Nom: ${d.get('nom')}\n📅 Date: ${d.get('date')}\n⏰ Heure: ${d.get('heure')}\n👥 Personnes: ${d.get('pers')}`;
              window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`, '_blank');
            }}>
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-xs uppercase font-bold text-zinc-500">Nom complet</label>
                  <input name="nom" required className="w-full bg-zinc-800 border-zinc-700 rounded-lg p-3" />
                </div>
                <div className="space-y-2">
                  <label className="text-xs uppercase font-bold text-zinc-500">Nb de personnes</label>
                  <input name="pers" type="number" defaultValue="2" min="1" className="w-full bg-zinc-800 border-zinc-700 rounded-lg p-3" />
                </div>
                <div className="space-y-2">
                  <label className="text-xs uppercase font-bold text-zinc-500">Date</label>
                  <input name="date" type="date" required className="w-full bg-zinc-800 border-zinc-700 rounded-lg p-3 text-white" />
                </div>
                <div className="space-y-2">
                  <label className="text-xs uppercase font-bold text-zinc-500">Heure</label>
                  <input name="heure" type="time" required className="w-full bg-zinc-800 border-zinc-700 rounded-lg p-3" />
                </div>
              </div>
              <button className="w-full py-4 bg-amber-500 text-black font-bold rounded-xl shadow-lg hover:bg-amber-400 transition-all">
                Confirmer sur WhatsApp
              </button>
            </form>
          </div>
        )}

        {/* VIEW: CART */}
        {view === 'cart' && (
          <div className="max-w-4xl mx-auto space-y-8 animate-in slide-in-from-right duration-500">
            <h1 className="text-4xl text-amber-500 text-center">Votre Panier</h1>
            
            {cart.length === 0 ? (
              <div className="text-center py-20 bg-zinc-900 rounded-3xl border border-zinc-800">
                <p className="text-zinc-500 mb-6">Votre panier est vide pour le moment.</p>
                <button onClick={() => setView('menu')} className="text-amber-500 underline">Retourner au menu</button>
              </div>
            ) : (
              <div className="grid md:grid-cols-3 gap-8">
                <div className="md:col-span-2 space-y-4">
                  {cart.map(item => (
                    <div key={item.id} className="flex items-center gap-4 bg-zinc-900 p-4 rounded-2xl border border-zinc-800">
                      <img src={item.image} className="w-20 h-20 rounded-xl object-cover" alt={item.name} />
                      <div className="flex-1">
                        <h4 className="font-bold">{item.name}</h4>
                        <p className="text-amber-500">{item.price} F × {item.quantity}</p>
                      </div>
                      <div className="flex flex-col gap-2">
                        <button onClick={() => removeFromCart(item.id)} className="p-2 text-zinc-500 hover:text-red-500">🗑️</button>
                      </div>
                    </div>
                  ))}
                  <div className="p-6 bg-zinc-900 rounded-2xl border border-zinc-800 flex justify-between items-center">
                    <span className="text-xl">Total</span>
                    <span className="text-2xl font-bold text-amber-500">{cartTotal} FCFA</span>
                  </div>
                </div>

                <div className="bg-zinc-900 p-6 rounded-3xl border border-zinc-800 h-fit">
                  <h3 className="text-xl mb-6 font-bold">Détails Livraison</h3>
                  <form onSubmit={handleCheckout} className="space-y-4">
                    <div className="space-y-2">
                      <label className="text-xs font-bold text-zinc-500">Option</label>
                      <select name="type" className="w-full bg-zinc-800 p-3 rounded-lg border-zinc-700">
                        <option value="Sur place">Sur place (Table)</option>
                        <option value="Livraison">Livraison à domicile</option>
                      </select>
                    </div>
                    <div className="space-y-2">
                      <label className="text-xs font-bold text-zinc-500">Table N° ou Adresse & Tél</label>
                      <textarea name="logistics" required className="w-full bg-zinc-800 p-3 rounded-lg border-zinc-700 min-h-[100px]" placeholder="Précisez ici..." />
                    </div>
                    <button className="w-full py-4 bg-green-500 text-white font-bold rounded-xl shadow-lg hover:bg-green-600 transition-all flex items-center justify-center gap-2">
                      <span>🚀</span> Valider la commande
                    </button>
                  </form>
                </div>
              </div>
            )}
          </div>
        )}

        {/* VIEW: ADMIN */}
        {view === 'admin' && (
          <div className="max-w-5xl mx-auto space-y-8 animate-in slide-in-from-top duration-500">
            <h1 className="text-4xl text-amber-500 text-center">Espace Gérant</h1>
            
            {adminCode !== ADMIN_PASS ? (
              <div className="max-w-xs mx-auto text-center space-y-4">
                <input 
                  type="password" 
                  placeholder="Code secret" 
                  onChange={(e) => setAdminCode(e.target.value)}
                  className="w-full bg-zinc-900 p-3 rounded-xl border border-zinc-700 text-center"
                />
                <p className="text-zinc-500 text-xs italic">Indice: admin123</p>
              </div>
            ) : (
              <div className="grid md:grid-cols-2 gap-8">
                <div className="space-y-6">
                  <h2 className="text-2xl text-amber-500">Ajouter un plat</h2>
                  <form className="bg-zinc-900 p-6 rounded-2xl border border-zinc-800 space-y-4" onSubmit={(e) => {
                    e.preventDefault();
                    const d = new FormData(e.currentTarget);
                    const newItem: MenuItem = {
                      id: Math.random().toString(36).substr(2, 9),
                      name: d.get('name') as string,
                      price: Number(d.get('price')),
                      description: d.get('desc') as string,
                      image: (d.get('img') as string) || 'https://via.placeholder.com/400x250',
                      category: 'Plat'
                    };
                    setMenu([...menu, newItem]);
                    e.currentTarget.reset();
                  }}>
                    <input name="name" placeholder="Nom du plat" required className="w-full bg-zinc-800 p-3 rounded-lg" />
                    <input name="price" type="number" placeholder="Prix (FCFA)" required className="w-full bg-zinc-800 p-3 rounded-lg" />
                    <input name="img" placeholder="Lien Image (URL)" className="w-full bg-zinc-800 p-3 rounded-lg" />
                    <textarea name="desc" placeholder="Description courte" className="w-full bg-zinc-800 p-3 rounded-lg" />
                    <button className="w-full py-3 bg-amber-500 text-black font-bold rounded-xl">Enregistrer</button>
                  </form>
                  
                  <h2 className="text-2xl text-amber-500 pt-8">Gérer la Carte</h2>
                  <div className="space-y-2">
                    {menu.map(m => (
                      <div key={m.id} className="flex items-center gap-4 bg-zinc-900 p-3 rounded-xl">
                        <img src={m.image} className="w-12 h-12 object-cover rounded-lg" alt={m.name} />
                        <span className="flex-1 text-sm">{m.name} ({m.price}F)</span>
                        <button onClick={() => setMenu(menu.filter(i => i.id !== m.id))} className="text-red-500">🗑️</button>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="space-y-6">
                  <h2 className="text-2xl text-amber-500">Historique Commandes</h2>
                  <div className="space-y-4">
                    {orders.length === 0 ? <p className="text-zinc-500">Aucune commande.</p> : orders.map(order => (
                      <div key={order.id} className="bg-zinc-900 p-4 rounded-xl border border-zinc-800 text-sm space-y-2">
                        <div className="flex justify-between font-bold text-amber-500">
                          <span>{new Date(order.timestamp).toLocaleString()}</span>
                          <span>{order.total} F</span>
                        </div>
                        <p className="text-zinc-400">{order.items.map(i => `${i.name} x${i.quantity}`).join(', ')}</p>
                        <p className="text-zinc-500 border-t border-zinc-800 pt-2">{order.type} - {order.logistics}</p>
                      </div>
                    ))}
                    <button 
                      onClick={() => setOrders([])} 
                      className="w-full py-2 text-red-500 text-xs uppercase font-bold hover:bg-red-500/10 rounded-lg transition-colors"
                    >
                      Effacer l'historique
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="py-8 border-t border-zinc-800 mt-12 text-center text-zinc-500 text-sm">
        <p>© 2024 Teranga Gourmet Express • Dakar, Sénégal</p>
        <div className="flex justify-center gap-4 mt-4">
          <a href={`tel:${CALL_NUMBER}`} className="text-amber-500">Appeler : {CALL_NUMBER}</a>
        </div>
      </footer>
    </div>
  );
};

export default App;
