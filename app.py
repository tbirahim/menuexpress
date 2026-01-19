import React, { useState, useEffect, useMemo } from 'react';
import { View, MenuItem, CartItem, Order } from './types';
import { INITIAL_MENU, WHATSAPP_NUMBER, CALL_NUMBER, ADMIN_PASS } from './constants';

const App: React.FC = () => {
  const [view, setView] = useState<View>('home');
  const [menu, setMenu] = useState<MenuItem[]>(() => {
    const saved = localStorage.getItem('tg_menu_v4');
    return saved ? JSON.parse(saved) : INITIAL_MENU;
  });
  const [cart, setCart] = useState<CartItem[]>([]);
  const [orders, setOrders] = useState<Order[]>(() => {
    const saved = localStorage.getItem('tg_orders_v4');
    return saved ? JSON.parse(saved) : [];
  });
  const [adminCode, setAdminCode] = useState("");
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  useEffect(() => { localStorage.setItem('tg_menu_v4', JSON.stringify(menu)); }, [menu]);
  useEffect(() => { localStorage.setItem('tg_orders_v4', JSON.stringify(orders)); }, [orders]);

  const addToCart = (item: MenuItem) => {
    setCart(prev => {
      const existing = prev.find(i => i.id === item.id);
      if (existing) return prev.map(i => i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i);
      return [...prev, { ...item, quantity: 1 }];
    });
  };

  const updateQuantity = (id: string, delta: number) => {
    setCart(prev => prev.map(item => item.id === id ? { ...item, quantity: Math.max(1, item.quantity + delta) } : item));
  };

  const removeFromCart = (id: string) => setCart(prev => prev.filter(i => i.id !== id));
  const cartTotal = useMemo(() => cart.reduce((acc, curr) => acc + (curr.price * curr.quantity), 0), [cart]);

  // Simulation d'un st.sidebar.radio
  const RadioNav = ({ options }: { options: { id: View, label: string }[] }) => (
    <div className="space-y-1">
      <p className="text-[14px] font-semibold mb-2 opacity-80">Navigation</p>
      {options.map(opt => (
        <button
          key={opt.id}
          onClick={() => setView(opt.id)}
          className={`w-full text-left px-3 py-1.5 rounded-lg text-[14px] transition-colors flex items-center gap-2 ${
            view === opt.id 
              ? 'bg-white/10 text-white font-medium' 
              : 'text-zinc-400 hover:bg-white/5 hover:text-zinc-200'
          }`}
        >
          <div className={`w-3 h-3 rounded-full border-2 flex items-center justify-center ${view === opt.id ? 'border-[#ff4b4b]' : 'border-zinc-600'}`}>
            {view === opt.id && <div className="w-1.5 h-1.5 rounded-full bg-[#ff4b4b]" />}
          </div>
          {opt.label}
        </button>
      ))}
    </div>
  );

  return (
    <div className="flex min-h-screen">
      
      {/* --- STREAMLIT SIDEBAR --- */}
      <aside className={`
        fixed md:relative inset-y-0 left-0 z-40 w-[260px] bg-[#262730] border-r border-white/5 p-6 flex flex-col transition-transform duration-300
        ${isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0 md:hidden'}
      `}>
        <div className="mb-10">
          <h1 className="text-xl font-bold flex items-center gap-2">
            <span className="text-[#ff4b4b]">T</span>eranga Web
          </h1>
          <p className="text-[12px] opacity-40 mt-1">Dakar, Sénégal</p>
        </div>

        <nav className="flex-1 space-y-8">
          <RadioNav options={[
            { id: 'home', label: '🏠 Accueil' },
            { id: 'menu', label: '🍴 La Carte' },
            { id: 'reserve', label: '📅 Réservations' },
            { id: 'cart', label: `🛒 Panier (${cart.length})` },
            { id: 'admin', label: '⚙️ Gestion Gérant' }
          ]} />
          
          <div className="pt-4 border-t border-white/5">
            <p className="text-[12px] font-bold uppercase tracking-widest text-zinc-500 mb-3">Service Client</p>
            <a href={`tel:${CALL_NUMBER}`} className="block text-[#ff4b4b] font-medium hover:underline text-sm">📞 {CALL_NUMBER}</a>
          </div>
        </nav>

        <div className="mt-auto pt-6 opacity-30 text-[10px] uppercase tracking-widest">
          v4.2.0 • Streamlit UI
        </div>
      </aside>

      {/* --- MAIN CONTENT --- */}
      <main className="flex-1 flex flex-col bg-[#0e1117] relative min-w-0">
        
        {/* Toggle mobile sidebar */}
        <button 
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          className="md:hidden fixed top-4 left-4 z-50 p-2 bg-[#262730] rounded-lg border border-white/10"
        >
          {isSidebarOpen ? '✕' : '☰'}
        </button>

        <div className="flex-1 overflow-y-auto px-6 py-12 md:px-16 md:py-16 max-w-4xl w-full mx-auto">
          
          {view === 'home' && (
            <div className="space-y-8 animate-fade-in">
              <h2 className="text-4xl font-bold leading-tight">Teranga Gourmet Express 🇸🇳</h2>
              <div className="p-4 bg-[#1e2329] border-l-4 border-blue-500 rounded text-sm text-blue-200">
                Bienvenue sur notre application de commande en ligne. Profitez du goût authentique du Sénégal livré chez vous.
              </div>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="st-card p-6 space-y-4">
                  <h3 className="text-xl font-bold text-[#ff4b4b]">Explorer le Menu</h3>
                  <p className="text-zinc-400 text-sm">Consultez nos spécialités : Thieboudienne, Yassa, Maffé et nos jus de fruits locaux.</p>
                  <button onClick={() => setView('menu')} className="px-4 py-1.5 border border-[#ff4b4b] text-[#ff4b4b] hover:bg-[#ff4b4b]/10 rounded-lg text-sm transition-colors">
                    Voir la carte
                  </button>
                </div>
                <div className="st-card p-6 space-y-4">
                  <h3 className="text-xl font-bold text-white">Réservation</h3>
                  <p className="text-zinc-400 text-sm">Réservez votre table en quelques secondes pour un dîner inoubliable.</p>
                  <button onClick={() => setView('reserve')} className="px-4 py-1.5 border border-white/20 text-white hover:bg-white/5 rounded-lg text-sm transition-colors">
                    Réserver
                  </button>
                </div>
              </div>

              <div className="mt-12 rounded-xl overflow-hidden shadow-2xl border border-white/5">
                <img src="https://images.unsplash.com/photo-1574484284002-952d92456975?q=80&w=1200" className="w-full h-[300px] object-cover opacity-80" alt="Teranga" />
              </div>
            </div>
          )}

          {view === 'menu' && (
            <div className="space-y-10 animate-fade-in">
              <div className="flex justify-between items-end">
                <h2 className="text-3xl font-bold">🍴 Carte du jour</h2>
                <div className="text-sm opacity-50">{menu.length} plats disponibles</div>
              </div>
              
              <div className="space-y-6">
                {menu.map(item => (
                  <div key={item.id} className="st-card p-4 flex flex-col sm:flex-row gap-6 hover:border-white/20 transition-all">
                    <img src={item.image} className="w-full sm:w-32 h-32 rounded-lg object-cover" alt={item.name} />
                    <div className="flex-1 flex flex-col justify-between">
                      <div>
                        <div className="flex justify-between items-start">
                          <h3 className="text-lg font-bold">{item.name}</h3>
                          <span className="text-[#ff4b4b] font-bold">{item.price.toLocaleString()} FCFA</span>
                        </div>
                        <p className="text-zinc-500 text-sm mt-1">{item.description}</p>
                      </div>
                      <div className="mt-4">
                        <button 
                          onClick={() => addToCart(item)}
                          className="px-4 py-1.5 bg-[#ff4b4b] text-white rounded-lg text-xs font-bold uppercase tracking-wider hover:opacity-90 transition-opacity"
                        >
                          Ajouter au panier
                        </button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {view === 'reserve' && (
            <div className="max-w-md space-y-10 animate-fade-in">
              <h2 className="text-3xl font-bold">📅 Réservation</h2>
              <form className="space-y-4" onSubmit={(e) => {
                e.preventDefault();
                const d = new FormData(e.currentTarget);
                const msg = `RÉSERVATION\nNom: ${d.get('nom')}\nDate: ${d.get('date')}\nHeure: ${d.get('heure')}\nCouverts: ${d.get('pers')}`;
                window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`, '_blank');
              }}>
                <div className="space-y-1">
                  <label className="text-sm font-medium opacity-70">Nom complet</label>
                  <input name="nom" required className="w-full bg-[#262730] border border-white/10 rounded-lg p-2.5 text-sm focus:border-[#ff4b4b] outline-none" />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <label className="text-sm font-medium opacity-70">Personnes</label>
                    <input name="pers" type="number" defaultValue="2" className="w-full bg-[#262730] border border-white/10 rounded-lg p-2.5 text-sm" />
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-medium opacity-70">Date</label>
                    <input name="date" type="date" required className="w-full bg-[#262730] border border-white/10 rounded-lg p-2.5 text-sm" />
                  </div>
                </div>
                <div className="space-y-1">
                  <label className="text-sm font-medium opacity-70">Heure souhaitée</label>
                  <input name="heure" type="time" required className="w-full bg-[#262730] border border-white/10 rounded-lg p-2.5 text-sm" />
                </div>
                <button type="submit" className="w-full py-3 bg-[#ff4b4b] text-white font-bold rounded-lg text-sm hover:opacity-90 mt-4 shadow-lg">
                  Confirmer sur WhatsApp
                </button>
              </form>
            </div>
          )}

          {view === 'cart' && (
            <div className="max-w-xl space-y-10 animate-fade-in">
              <h2 className="text-3xl font-bold">🛒 Votre Commande</h2>
              {cart.length === 0 ? (
                <div className="p-8 text-center st-card opacity-50 italic">Votre panier est vide.</div>
              ) : (
                <div className="space-y-8">
                  <div className="space-y-2">
                    {cart.map(item => (
                      <div key={item.id} className="st-card p-4 flex justify-between items-center">
                        <div>
                          <p className="font-bold">{item.name}</p>
                          <p className="text-[#ff4b4b] text-xs font-bold">{item.price.toLocaleString()} F</p>
                        </div>
                        <div className="flex items-center gap-4">
                          <div className="flex items-center gap-2 bg-black/30 rounded-lg px-2 py-1">
                            <button onClick={() => updateQuantity(item.id, -1)} className="hover:text-[#ff4b4b]">-</button>
                            <span className="text-xs font-mono w-4 text-center">{item.quantity}</span>
                            <button onClick={() => updateQuantity(item.id, 1)} className="hover:text-[#ff4b4b]">+</button>
                          </div>
                          <button onClick={() => removeFromCart(item.id)} className="text-zinc-600 hover:text-red-400">✕</button>
                        </div>
                      </div>
                    ))}
                  </div>

                  <div className="p-5 st-card border-l-4 border-green-500 flex justify-between items-center">
                    <span className="font-medium opacity-60">Total à payer</span>
                    <span className="text-2xl font-black">{cartTotal.toLocaleString()} FCFA</span>
                  </div>

                  <form className="space-y-4 pt-4" onSubmit={(e) => {
                    e.preventDefault();
                    const d = new FormData(e.currentTarget);
                    const itemsTxt = cart.map(i => `- ${i.name} (x${i.quantity})`).join('\n');
                    const fullMsg = `COMMANDE\n${itemsTxt}\nTotal: ${cartTotal} F\nMode: ${d.get('type')}\nLieu: ${d.get('logistics')}`;
                    window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(fullMsg)}`, '_blank');
                    setCart([]); setView('home');
                  }}>
                    <div className="space-y-1">
                      <label className="text-sm font-medium opacity-70">Type de service</label>
                      <select name="type" className="w-full bg-[#262730] border border-white/10 rounded-lg p-2.5 text-sm outline-none">
                        <option value="Sur place">Manger sur place</option>
                        <option value="Livraison">Livraison à domicile</option>
                      </select>
                    </div>
                    <div className="space-y-1">
                      <label className="text-sm font-medium opacity-70">Précisions (Table ou Adresse)</label>
                      <textarea name="logistics" required className="w-full bg-[#262730] border border-white/10 rounded-lg p-2.5 text-sm min-h-[80px]" />
                    </div>
                    <button type="submit" className="w-full py-4 bg-green-600 text-white font-bold rounded-lg hover:bg-green-500 shadow-xl">
                      Passer ma commande
                    </button>
                  </form>
                </div>
              )}
            </div>
          )}

          {view === 'admin' && (
            <div className="space-y-10 animate-fade-in">
              <h2 className="text-3xl font-bold">⚙️ Gestion Administrateur</h2>
              {adminCode !== ADMIN_PASS ? (
                <div className="max-w-xs space-y-4">
                  <p className="text-sm opacity-50">Authentification requise.</p>
                  <input 
                    type="password" 
                    placeholder="Entrez le code..." 
                    onChange={(e) => setAdminCode(e.target.value)} 
                    className="w-full bg-[#262730] border border-white/10 rounded-lg p-3 text-center tracking-[0.5em] focus:border-[#ff4b4b] outline-none"
                  />
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                  <div className="space-y-6">
                    <h3 className="text-lg font-bold border-b border-white/5 pb-2">Ajouter un plat</h3>
                    <form className="space-y-3 bg-[#262730]/50 p-6 rounded-xl border border-white/5" onSubmit={(e) => {
                      e.preventDefault();
                      const d = new FormData(e.currentTarget);
                      setMenu([...menu, { 
                        id: Math.random().toString(36).substring(2, 9), 
                        name: d.get('name') as string, 
                        price: Number(d.get('price')), 
                        description: d.get('desc') as string, 
                        image: (d.get('img') as string) || 'https://via.placeholder.com/400x250', 
                        category: 'Plat' 
                      }]);
                      e.currentTarget.reset();
                    }}>
                      <input name="name" required placeholder="Nom du produit" className="w-full bg-[#0e1117] border border-white/5 rounded p-2 text-sm" />
                      <input name="price" type="number" required placeholder="Prix (FCFA)" className="w-full bg-[#0e1117] border border-white/5 rounded p-2 text-sm" />
                      <input name="img" placeholder="Lien image" className="w-full bg-[#0e1117] border border-white/5 rounded p-2 text-sm" />
                      <textarea name="desc" placeholder="Description" className="w-full bg-[#0e1117] border border-white/5 rounded p-2 text-sm" />
                      <button className="w-full py-2 bg-[#ff4b4b] text-white rounded text-xs font-bold uppercase">Sauvegarder</button>
                    </form>
                  </div>
                  <div className="space-y-6 opacity-40 italic text-sm">
                    <p>Statistiques et historique masqués en mode Streamlit Lite.</p>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        <footer className="mt-auto p-10 text-center opacity-10 text-[10px] uppercase tracking-[1em]">
          Teranga Web Express • Dakar 2024
        </footer>
      </main>
    </div>
  );
};

export default App;
