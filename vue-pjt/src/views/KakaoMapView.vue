<template>
  <div>
    <h2 class="MainText">주변 은행</h2>

      <div id="map"></div>
      <div id="placesList"></div>
  
    <div class="input">
      <div class="input-group mb-3">
        <input
          type="text"
          class="form-control"
          placeholder="도시 또는 은행 입력"
          v-model="searchQuery"
          @keyup.enter="searchPlaces"
        />
        <button class="btn btn-primary" @click="searchPlaces">검색</button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
const API_KEY = import.meta.env.VITE_API_KEY;
export default {
  name: "KakaoMap",
  mounted() {
    // 카카오맵 API 스크립트 로드
    let script = document.createElement("script");
    script.type = "text/javascript";
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${API_KEY}&autoload=false&libraries=services,clusterer,drawing`;

    document.head.appendChild(script);

    script.onload = () => {
      kakao.maps.load(() => {
        this.loadKakaoMap();
      });
    };
  },
  data() {
    return {
      searchQuery: "역삼역",
      map: null,
      infowindow: null,
      markers: [],
    };
  },

  methods: {
    loadKakaoMap() {
      let mapContainer = document.getElementById("map");
      let mapOption = {
        center: new kakao.maps.LatLng(37.5013, 127.0397),
        level: 5,
      };

      this.map = new kakao.maps.Map(mapContainer, mapOption);
      this.infowindow = new kakao.maps.InfoWindow({ zIndex: 1 });
      this.searchPlaces();
      this.addMarker();
    },
    searchPlaces() {
      const ps = new kakao.maps.services.Places(this.map);
      const options = {
        category_group_code: "BK9",
      };
      ps.keywordSearch(
        this.searchQuery,
        (data, status) => {
          console.log(data);
          if (status === kakao.maps.services.Status.OK) {
            const banks = data.filter(
              (place) => place.category_group_code === "BK9"
            );
            this.displayMarkers(banks);
          } else if (status === kakao.maps.services.Status.ZERO_RESULT) {
            alert("검색 결과가 존재하지 않습니다");
            return;
          } else if (status === kakao.maps.services.Status.ERROR) {
            alert("검색 결과 중 오류가 발생했습니다.");
            return;
          }
        },
        options
      );
    },
    clearMarkers() {
      if (this.markers) {
        this.markers.forEach((marker) => {
          marker.setMap(null);
        });
        this.markers = [];
      }
    },
    displayMarkers(places) {
      this.clearMarkers();
      if (places.length > 0) {
        let listEl = document.getElementById("placesList");
        listEl.innerHTML = "";
        let bounds = new kakao.maps.LatLngBounds();

        places.forEach((place) => {
          let marker = new kakao.maps.Marker({
            map: this.map,
            position: new kakao.maps.LatLng(place.y, place.x),
          });

          kakao.maps.event.addListener(marker, "mouseover", () => {
            this.infowindow.setContent(
              '<div style="padding:5px;font-size:12px;">' +
                place.place_name +
                "</div>"
            );
            this.infowindow.open(this.map, marker);
          });

          kakao.maps.event.addListener(marker, "mouseout", () => {
            this.infowindow.close();
          });

          // 목록 추가
          let listItem = getListItem(places.indexOf(place), place);
          console.log(listItem);
          listEl.appendChild(listItem);
          console.log(listEl);

          // 지도 영역 설정
          bounds.extend(new kakao.maps.LatLng(place.y, place.x));
        });
        this.map.setBounds(bounds);

        function getListItem(index, place) {
          var el = document.createElement("li"),
            itemStr =
              '<span class="markerbg marker_' +
              (index + 1) +
              '"></span>' +
              '<div class="info">' +
              "   <h5>" +
              place.place_name +
              "</h5>";

          if (place.road_address_name) {
            itemStr +=
              "    <span>" +
              place.road_address_name +
              "</span>" +
              '   <span class="jibun gray">' +
              place.address_name +
              "</span>";
          } else {
            itemStr += "    <span>" + place.address_name + "</span>";
          }

          itemStr +=
            '  <span class="tel">' + place.phone + "</span>" + "</div>";

          el.innerHTML = itemStr;
          el.className = "item";

          return el;
        }
      }
    },
  },
};
</script>

<style scoped>
.input {
  display: flex;
  justify-content: center;
  width: 300px;
  margin: 50px auto;
}

#map {
  margin: 50px auto;
  width: 500px;
  height: 400px;
}

#placesList {
  max-height: 400px;
  overflow-y: auto;
  margin: 10px 0; /* Adjust the margin based on your layout */
}
.MainText {
  text-align: center;
}

.text {
  margin-right: 10px;
}
</style>
