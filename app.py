
import React, { useState, useEffect, useMemo } from 'react';
import { View, MenuItem, CartItem, Order } from './types';
import { INITIAL_MENU, WHATSAPP_NUMBER, CALL_NUMBER, ADMIN_PASS } from './constants';

// --- Icons (Streamlit Style - Simple & Clean) ---
const Icons = {
  Home: () => <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>,
  Menu: () => <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>,
  Reserve: () => <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect width="18" height="18" x="3" y="4" rx="2" ry="2"/><line x1="16" x2="16" y1="2" y2="6"/><line x1="8" x2="8" y1="2" y2="6"/><line x1="3" x2="21" y1="10" y2="10"/></svg>,
  Cart: () => <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="8" cy="21" r="1"/><circle cx="19" cy="21" r="1"/><path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12"/></svg>,
  Admin: () => <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/></svg>,
  Trash: () => <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/></svg>
};

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
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => { localStorage.setItem('tg_menu_v4', JSON.stringify(menu)); }, [menu]);
  useEffect(() => { localStorage.setItem('tg_orders_v4', JSON.stringify(orders)); }, [orders]);

  const addToCart = (item: MenuItem) => {
    setCart(prev => {
      const existing = prev.find(i => i.id === item.id);
      if (existing) return prev.map(i => i.id === item.id ? { ...i, quantity: i.quantity + 1 } : i);
      return [...prev, { ...item, quantity: 1 }];
    });
    setView('cart'); // Redirection automatique comme dans les apps simples
  };

  const updateQuantity = (id: string, delta: number) => {
    setCart(prev => prev.map(item => item.id === id ? { ...item, quantity: Math.max(1, item.quantity + delta) } : item));
  };

  const removeFromCart = (id: string) => setCart(prev => prev.filter(i => i.id !== id));
  const cartTotal = useMemo(() => cart.reduce((acc, curr) => acc + (curr.price * curr.quantity), 0), [cart]);

  const NavButton: React.FC<{ v: View, icon: React.ReactNode, label: string }> = ({ v, icon, label }) => (
    <button 
      onClick={() => { setView(v); setIsMobileMenuOpen(false); }}
      className={`w-full flex items-center gap-3 px-4 py-2 rounded-lg transition-colors text-sm font-medium ${view === v ? 'bg-zinc-700 text-white' : 'text-zinc-400 hover:bg-zinc-800 hover:text-zinc-200'}`}
    >
      {icon} {label}
    </button>
  );

  return (
    <div className="flex flex-col md:flex-row min-h-screen bg-[#0e1117] text-[#fafafa] font-sans selection:bg-amber-500/30">
      
      {/* --- SIDEBAR (Desktop) / TOPBAR (Mobile) --- */}
      <aside className={`
        fixed inset-y-0 left-0 z-50 w-64 bg-[#262730] border-r border-white/5 p-6 space-y-8 transform transition-transform duration-200 ease-in-out
        ${isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'}
        md:relative md:translate-x-0
      `}>
        <div className="flex items-center gap-3 mb-10">
          <div className="w-8 h-8 bg-amber-500 rounded flex items-center justify-center text-[#262730] font-black">T</div>
          <h1 className="text-xl font-bold tracking-tight">Teranga Web</h1>
        </div>

        <nav className="space-y-2">
          <p className="text-[10px] uppercase tracking-widest text-zinc-500 font-bold mb-4 px-2">Navigation</p>
          <NavButton v="home" icon={<Icons.Home />} label="Accueil" />
          <NavButton v="menu" icon={<Icons.Menu />} label="La Carte" />
          <NavButton v="reserve" icon={<Icons.Reserve />} label="Réservations" />
          <NavButton v="cart" icon={<Icons.Cart />} label={`Panier (${cart.length})`} />
          <div className="pt-8">
            <p className="text-[10px] uppercase tracking-widest text-zinc-500 font-bold mb-4 px-2">Administration</p>
            <NavButton v="admin" icon={<Icons.Admin />} label="Gestion" />
          </div>
        </nav>

        <div className="absolute bottom-6 left-6 right-6">
           <div className="p-4 bg-zinc-800/50 rounded-lg border border-white/5">
             <p className="text-[10px] text-zinc-500 uppercase font-bold mb-1">Contact Rapide</p>
             <a href={`tel:${CALL_NUMBER}`} className="text-amber-500 font-bold text-sm hover:underline">{CALL_NUMBER}</a>
           </div>
        </div>
      </aside>

      {/* --- MOBILE TOGGLE --- */}
      <div className="md:hidden bg-[#262730] p-4 flex justify-between items-center border-b border-white/5">
        <div className="flex items-center gap-2">
           <div className="w-6 h-6 bg-amber-500 rounded flex items-center justify-center text-xs font-black">T</div>
           <span className="font-bold">Teranga Web</span>
        </div>
        <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)} className="p-2 text-zinc-400">
          <Icons.Menu />
        </button>
      </div>

      {/* --- MAIN CONTENT --- */}
      <main className="flex-1 overflow-y-auto p-6 md:p-12 max-w-5xl mx-auto w-full">
        
        {view === 'home' && (
          <div className="space-y-10 animate-fade-in">
            <div className="space-y-4">
              <h2 className="text-4xl md:text-5xl font-extrabold text-white tracking-tight">Bienvenue à la Teranga 🇸🇳</h2>
              <p className="text-zinc-400 text-lg leading-relaxed max-w-2xl">
                Découvrez l'authenticité de la cuisine sénégalaise. Des produits frais, des recettes ancestrales et une livraison rapide partout à Dakar.
              </p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <button onClick={() => setView('menu')} className="p-8 bg-zinc-800/40 border border-white/5 rounded-2xl text-left hover:bg-zinc-800/60 transition-all group">
                <h3 className="text-xl font-bold text-amber-500 mb-2 group-hover:translate-x-1 transition-transform">Consulter le Menu →</h3>
                <p className="text-zinc-500 text-sm">Thieboudienne, Yassa, Maffé et bien plus encore.</p>
              </button>
              <button onClick={() => setView('reserve')} className="p-8 bg-zinc-800/40 border border-white/5 rounded-2xl text-left hover:bg-zinc-800/60 transition-all group">
                <h3 className="text-xl font-bold text-white mb-2 group-hover:translate-x-1 transition-transform">Réserver une Table →</h3>
                <p className="text-zinc-500 text-sm">Planifiez votre moment privilégié chez nous.</p>
              </button>
            </div>

            <hr className="border-white/5" />

            <div className="rounded-2xl overflow-hidden h-[300px] shadow-2xl relative">
              <img src="https://images.unsplash.com/photo-1574484284002-952d92456975?q=80&w=1200" className="w-full h-full object-cover" alt="Plat Signature" />
              <div className="absolute inset-0 bg-gradient-to-t from-[#0e1117] to-transparent"></div>
              <p className="absolute bottom-6 left-6 font-bold text-xl italic text-white">"La saveur du pays, à votre table."</p>
            </div>
          </div>
        )}

        {view === 'menu' && (
          <div className="space-y-10 animate-fade-in">
            <h2 className="text-3xl font-extrabold text-white">Notre Carte</h2>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
              {menu.map(item => (
                <div key={item.id} className="bg-[#262730] rounded-xl overflow-hidden border border-white/5 flex flex-col sm:flex-row h-full">
                  <img src={item.image} className="w-full sm:w-32 h-40 sm:h-full object-cover" alt={item.name} />
                  <div className="p-5 flex-1 flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-start mb-2">
                        <h3 className="font-bold text-white">{item.name}</h3>
                        <span className="text-amber-500 font-bold text-sm whitespace-nowrap">{item.price.toLocaleString()} F</span>
                      </div>
                      <p className="text-zinc-500 text-xs leading-relaxed mb-4">{item.description}</p>
                    </div>
                    <button 
                      onClick={() => addToCart(item)}
                      className="w-full py-2 bg-zinc-700 hover:bg-zinc-600 text-white text-[10px] font-bold uppercase tracking-widest rounded-lg transition-colors"
                    >
                      Ajouter au panier
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {view === 'reserve' && (
          <div className="max-w-xl space-y-10 animate-fade-in">
            <h2 className="text-3xl font-extrabold text-white">Réservation</h2>
            <form className="space-y-6" onSubmit={(e) => {
              e.preventDefault();
              const d = new FormData(e.currentTarget);
              const msg = `RÉSERVATION\nNom: ${d.get('nom')}\nDate: ${d.get('date')}\nHeure: ${d.get('heure')}\nCouverts: ${d.get('pers')}`;
              window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(msg)}`, '_blank');
            }}>
              <div className="space-y-2">
                <label className="text-sm font-medium text-zinc-400">Nom complet</label>
                <input name="nom" required placeholder="Votre nom" className="w-full bg-[#262730] border border-white/10 rounded-lg p-3 text-sm focus:border-amber-500 outline-none" />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium text-zinc-400">Nombre de personnes</label>
                  <input name="pers" type="number" defaultValue="2" min="1" className="w-full bg-[#262730] border border-white/10 rounded-lg p-3 text-sm" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-medium text-zinc-400">Date</label>
                  <input name="date" type="date" required className="w-full bg-[#262730] border border-white/10 rounded-lg p-3 text-sm" />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-medium text-zinc-400">Heure</label>
                <input name="heure" type="time" required className="w-full bg-[#262730] border border-white/10 rounded-lg p-3 text-sm" />
              </div>
              <button className="w-full py-4 bg-amber-500 text-[#262730] font-black rounded-lg uppercase text-xs tracking-widest hover:bg-amber-400 transition-colors">
                Réserver sur WhatsApp
              </button>
            </form>
          </div>
        )}

        {view === 'cart' && (
          <div className="max-w-2xl space-y-10 animate-fade-in">
            <h2 className="text-3xl font-extrabold text-white">Votre Panier</h2>
            {cart.length === 0 ? (
              <div className="p-12 text-center bg-[#262730] rounded-2xl border border-white/5 space-y-4">
                <p className="text-zinc-500">Votre panier est tristement vide.</p>
                <button onClick={() => setView('menu')} className="text-amber-500 font-bold hover:underline">Découvrir le menu</button>
              </div>
            ) : (
              <div className="space-y-8">
                <div className="space-y-3">
                  {cart.map(item => (
                    <div key={item.id} className="flex items-center gap-4 bg-[#262730] p-4 rounded-xl border border-white/5">
                      <div className="flex-1">
                        <p className="font-bold text-sm">{item.name}</p>
                        <p className="text-amber-500 text-xs">{item.price.toLocaleString()} F</p>
                      </div>
                      <div className="flex items-center gap-4">
                         <div className="flex items-center gap-2 bg-black/20 rounded-lg px-2 py-1">
                           <button onClick={() => updateQuantity(item.id, -1)} className="text-zinc-400 hover:text-white">-</button>
                           <span className="text-xs font-bold w-4 text-center">{item.quantity}</span>
                           <button onClick={() => updateQuantity(item.id, 1)} className="text-zinc-400 hover:text-white">+</button>
                         </div>
                         <button onClick={() => removeFromCart(item.id)} className="text-zinc-600 hover:text-red-400"><Icons.Trash /></button>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="p-6 bg-[#262730] rounded-xl border-l-4 border-amber-500 flex justify-between items-center">
                   <span className="text-zinc-400 font-medium">Total Commande</span>
                   <span className="text-2xl font-black text-white">{cartTotal.toLocaleString()} F</span>
                </div>

                <form onSubmit={(e) => {
                  e.preventDefault();
                  const d = new FormData(e.currentTarget);
                  const newOrder: Order = { id: Math.random().toString(36).substring(2, 9), items: [...cart], total: cartTotal, type: d.get('type') as any, logistics: d.get('logistics') as string, timestamp: Date.now() };
                  setOrders([newOrder, ...orders]);
                  const itemsTxt = cart.map(i => `- ${i.name} (x${i.quantity})`).join('\n');
                  const fullMsg = `COMMANDE\n${itemsTxt}\nTotal: ${cartTotal} F\nMode: ${d.get('type')}\nInfos: ${d.get('logistics')}`;
                  window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(fullMsg)}`, '_blank');
                  setCart([]); setView('home');
                }} className="space-y-6 pt-6">
                   <div className="space-y-2">
                     <label className="text-sm font-medium text-zinc-400">Mode de service</label>
                     <select name="type" className="w-full bg-[#262730] border border-white/10 rounded-lg p-3 text-sm">
                       <option value="Sur place">À table</option>
                       <option value="Livraison">Livraison</option>
                     </select>
                   </div>
                   <div className="space-y-2">
                     <label className="text-sm font-medium text-zinc-400">Adresse ou Numéro de table</label>
                     <textarea name="logistics" required className="w-full bg-[#262730] border border-white/10 rounded-lg p-3 text-sm min-h-[80px]" />
                   </div>
                   <button className="w-full py-4 bg-green-600 text-white font-black rounded-lg uppercase text-xs tracking-widest hover:bg-green-500 transition-colors">
                     Finaliser ma commande
                   </button>
                </form>
              </div>
            )}
          </div>
        )}

        {view === 'admin' && (
          <div className="max-w-4xl space-y-10 animate-fade-in">
            <h2 className="text-3xl font-extrabold text-white">Espace de Gestion</h2>
            {adminCode !== ADMIN_PASS ? (
              <div className="max-w-sm space-y-4">
                <p className="text-sm text-zinc-500 italic">Veuillez entrer le code d'accès gérant.</p>
                <input type="password" placeholder="••••" onChange={(e) => setAdminCode(e.target.value)} className="w-full bg-[#262730] border border-white/10 rounded-lg p-4 text-center tracking-[1em] focus:border-amber-500 outline-none" />
              </div>
            ) : (
              <div className="grid md:grid-cols-2 gap-12">
                <div className="space-y-6">
                  <h3 className="text-xl font-bold text-amber-500">Ajouter un produit</h3>
                  <form className="space-y-4 bg-[#262730] p-6 rounded-2xl border border-white/5" onSubmit={(e) => {
                    e.preventDefault();
                    const d = new FormData(e.currentTarget);
                    setMenu([...menu, { id: Math.random().toString(36).substring(2, 9), name: d.get('name') as string, price: Number(d.get('price')), description: d.get('desc') as string, image: (d.get('img') as string) || 'https://via.placeholder.com/400x250', category: 'Plat' }]);
                    e.currentTarget.reset();
                  }}>
                    <input name="name" required placeholder="Nom du plat" className="w-full bg-[#0e1117] border border-white/5 rounded-lg p-3 text-sm" />
                    <input name="price" type="number" required placeholder="Prix" className="w-full bg-[#0e1117] border border-white/5 rounded-lg p-3 text-sm" />
                    <input name="img" placeholder="Lien image" className="w-full bg-[#0e1117] border border-white/5 rounded-lg p-3 text-sm" />
                    <textarea name="desc" placeholder="Description courte" className="w-full bg-[#0e1117] border border-white/5 rounded-lg p-3 text-sm min-h-[80px]" />
                    <button className="w-full py-3 bg-amber-500 text-[#262730] font-black rounded-lg uppercase text-[10px] tracking-widest">Enregistrer</button>
                  </form>
                </div>

                <div className="space-y-6">
                  <h3 className="text-xl font-bold text-white">Historique local</h3>
                  <div className="space-y-4 max-h-[500px] overflow-y-auto pr-2 no-scrollbar">
                    {orders.map(o => (
                      <div key={o.id} className="bg-[#262730] p-4 rounded-xl border border-white/5 space-y-2">
                        <div className="flex justify-between text-[10px] font-bold text-zinc-500 uppercase">
                          <span>{new Date(o.timestamp).toLocaleDateString()}</span>
                          <span className="text-amber-500">{o.total.toLocaleString()} F</span>
                        </div>
                        <p className="text-xs text-white font-medium">{o.items.map(i => `${i.name} x${i.quantity}`).join(', ')}</p>
                        <p className="text-[10px] text-zinc-600 italic">{o.logistics}</p>
                      </div>
                    ))}
                    {orders.length === 0 && <p className="text-zinc-600 text-sm italic">Aucune commande enregistrée ici.</p>}
                  </div>
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="fixed bottom-4 right-6 text-[9px] uppercase tracking-[0.3em] text-zinc-700 hidden md:block">
        Teranga Web • Dakar 2024
      </footer>
    </div>
  );
};

export default App;
