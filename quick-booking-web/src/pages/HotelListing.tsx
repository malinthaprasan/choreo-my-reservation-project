import React, { useState } from 'react';

interface Hotel {
  id: number;
  name: string;
  imageUrl: string;
  description: string;
  rating: number;
  price: number;
  amenities: string[];
  location: string;
}

const HotelListing: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState('');

  // Sample hotel data - this would typically come from an API
  const hotels: Hotel[] = [
    { 
      id: 1, 
      name: "Grand Hotel",
      imageUrl: "https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
      description: "Experience luxury in the heart of the city. This 5-star hotel offers spectacular views and world-class service.",
      rating: 4.8,
      price: 299,
      amenities: ["Free WiFi", "Spa", "Pool", "Restaurant", "Gym"],
      location: "Downtown"
    },
    { 
      id: 2, 
      name: "Seaside Resort",
      imageUrl: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
      description: "Escape to paradise with our beachfront resort. Wake up to stunning ocean views and pristine beaches.",
      rating: 4.6,
      price: 399,
      amenities: ["Beach Access", "Pool", "Spa", "Water Sports", "Bar"],
      location: "Beachfront"
    },
    { 
      id: 3, 
      name: "Mountain Lodge",
      imageUrl: "https://images.unsplash.com/photo-1517840901100-8179e982acb7?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
      description: "A cozy retreat nestled in the mountains. Perfect for nature lovers and adventure seekers.",
      rating: 4.7,
      price: 249,
      amenities: ["Hiking Trails", "Fireplace", "Restaurant", "Parking"],
      location: "Mountain Range"
    },
    { 
      id: 4, 
      name: "City Center Hotel",
      imageUrl: "https://images.unsplash.com/photo-1496417263034-38ec4f0b665a?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60",
      description: "Modern comfort meets urban convenience. Steps away from shopping, dining and entertainment.",
      rating: 4.5,
      price: 199,
      amenities: ["Business Center", "Restaurant", "Fitness Center", "Parking", "Room Service"],
      location: "City Center"
    }
  ];

  const filteredHotels = hotels.filter(hotel =>
    hotel.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="hotel-listing">
      <div className="header">
        <h1>Quick Booking</h1>
      </div>
      <p className="subtitle">Your Perfect Stay Awaits. Discover amazing deals on hotels worldwide</p>
      
      <div className="search-container">
        <input
          type="text"
          placeholder="Search hotels..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      <div className="hotel-grid">
        {filteredHotels.map(hotel => (
          <div key={hotel.id} className="hotel-card">
            <div className="hotel-image-container">
              <img src={hotel.imageUrl} alt={hotel.name} className="hotel-image" />
              <span className="location-badge">{hotel.location}</span>
            </div>
            <div className="hotel-content">
              <h2>{hotel.name}</h2>
              <p className="description">{hotel.description}</p>
              <div className="rating">
                <span className="rating-score">{hotel.rating}</span>
                <span className="rating-text">Excellent</span>
              </div>
              <div className="amenities">
                {hotel.amenities.map((amenity, index) => (
                  <span key={index} className="amenity-tag">{amenity}</span>
                ))}
              </div>
              <div className="price-section">
                <span className="price">Starting from ${hotel.price}</span>
                <span className="per-night">per night</span>
              </div>
              <button className="book-button">Book Now</button>
            </div>
          </div>
        ))}
      </div>

      <style>{`
        .hotel-listing {
          padding: 40px;
          background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
          min-height: 100vh;
        }

        .header {
          text-align: center;
          margin-bottom: 20px;
        }

        .header h1 {
          color: #2c3e50;
          font-size: 3rem;
          margin-bottom: 5px;
          text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
          background: linear-gradient(45deg, #2c3e50, #3498db);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }

        .header h2 {
          color: #576574;
          font-size: 1.5rem;
          font-weight: normal;
          margin: 0;
        }

        .subtitle {
          text-align: center;
          color: #576574;
          font-size: 1.2rem;
          margin-bottom: 30px;
        }

        .search-container {
          max-width: 600px;
          margin: 0 auto 30px auto;
          padding: 0 20px;
        }

        .search-input {
          width: 100%;
          padding: 15px 20px;
          font-size: 1.1rem;
          border: none;
          border-radius: 25px;
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
          background: white;
          transition: all 0.3s ease;
        }

        .search-input:focus {
          outline: none;
          box-shadow: 0 6px 16px rgba(0,0,0,0.15);
          transform: translateY(-2px);
        }
        
        .hotel-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
          gap: 30px;
          padding: 20px;
          max-width: 1400px;
          margin: 0 auto;
        }
        
        .hotel-card {
          border: none;
          border-radius: 15px;
          overflow: hidden;
          background: rgba(255, 255, 255, 0.95);
          box-shadow: 0 10px 20px rgba(0,0,0,0.1);
          transition: all 0.3s ease;
        }
        
        .hotel-card:hover {
          transform: translateY(-10px);
          box-shadow: 0 15px 30px rgba(0,0,0,0.15);
        }

        .hotel-image-container {
          position: relative;
        }

        .hotel-image {
          width: 100%;
          height: 220px;
          object-fit: cover;
        }

        .location-badge {
          position: absolute;
          bottom: 10px;
          left: 10px;
          background: rgba(0,0,0,0.7);
          color: white;
          padding: 5px 10px;
          border-radius: 15px;
          font-size: 0.8rem;
        }
        
        .hotel-content {
          padding: 20px;
        }

        .hotel-card h2 {
          margin: 0 0 10px 0;
          font-size: 1.4rem;
          color: #34495e;
          font-weight: 600;
        }

        .description {
          color: #576574;
          font-size: 0.9rem;
          line-height: 1.5;
          margin-bottom: 15px;
        }

        .rating {
          display: flex;
          align-items: center;
          margin-bottom: 15px;
        }

        .rating-score {
          background: #003580;
          color: white;
          padding: 5px 10px;
          border-radius: 5px;
          margin-right: 10px;
          font-weight: bold;
        }

        .rating-text {
          color: #003580;
          font-weight: 500;
        }

        .amenities {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          margin-bottom: 15px;
        }

        .amenity-tag {
          background: #f1f2f6;
          color: #576574;
          padding: 4px 8px;
          border-radius: 12px;
          font-size: 0.8rem;
        }

        .price-section {
          margin-bottom: 15px;
        }

        .price {
          font-size: 1.3rem;
          font-weight: bold;
          color: #2d3436;
          margin-right: 5px;
        }

        .per-night {
          color: #576574;
          font-size: 0.9rem;
        }

        .book-button {
          width: 100%;
          padding: 12px;
          background: #003580;
          color: white;
          border: none;
          border-radius: 8px;
          font-size: 1rem;
          font-weight: 600;
          cursor: pointer;
          transition: all 0.3s ease;
        }

        .book-button:hover {
          background: #00224f;
          transform: translateY(-2px);
        }

        @media (max-width: 768px) {
          .hotel-listing {
            padding: 20px;
          }

          .header h1 {
            font-size: 2.5rem;
          }

          .header h2 {
            font-size: 1.2rem;
          }

          .hotel-grid {
            gap: 20px;
            padding: 10px;
          }

          .search-container {
            padding: 0 10px;
          }

          .hotel-card {
            margin-bottom: 20px;
          }
        }
      `}</style>
    </div>
  );
};

export default HotelListing;
