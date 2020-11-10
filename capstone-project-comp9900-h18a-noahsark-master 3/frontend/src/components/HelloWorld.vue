<template>

  <el-container class="homeContainer">
    <!------------------------- header ----------------------------->
    <div class="fixedHeader">
      <el-header>
        <div>
          <span id="brandName">Filmfinder</span>
        </div>

        <div id="searchBar">
          <el-input v-model="input" placeholder="Search for movies"></el-input>
          <el-button type="success" icon="el-icon-search">Search</el-button>
        </div>

        <div class="userInfo">
          <el-button type="danger" icon="el-icon-folder-delete" title="Blocklist" circle></el-button>
          <el-button type="warning" icon="el-icon-star-off" title="Wishlist" circle></el-button>
          <template>
            <el-button class="userInfo" type="text" @click="open">Sign up</el-button>
          </template>
          <el-button class="userInfo" type="text">Login</el-button>
        </div>
      </el-header>
    </div>
<!---------------------------------- main ----------------------------------->
    <el-main>
    <el-carousel :interval="4000" type="card" height="400px" indicator-position="outside">
      <el-carousel-item v-for="item in imagesBox" :key="item.id">
        <img :src="item.idView" class="img">
      </el-carousel-item>
        <el-aside id="showAside" width="100%">
          <div class="showDiv">
            <span id="showText">
              Elsa the Snow Queen has an extraordinary gift -- the power to create ice and snow. But no matter how happy she is to be surrounded by the people of Arendelle, Elsa finds herself strangely unsettled. After hearing a mysterious voice call out to her, Elsa travels to the enchanted forests and dark seas beyond her kingdom -- an adventure that soon turns into a journey of self-discovery.
            </span>
          </div>
        </el-aside>
      </el-carousel>

      <el-menu
        :default-active="activeIndex2"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b">

        <el-submenu index="1">
          <template slot="title">Now showing</template>
          <el-menu-item index="1-1">1</el-menu-item>
          <el-menu-item index="1-2">2</el-menu-item>
          <el-menu-item index="1-3">3</el-menu-item>
        </el-submenu>
        <el-submenu index="2">
          <template slot="title">Coming soon</template>
          <el-menu-item index="2-1">1</el-menu-item>
          <el-menu-item index="2-2">2</el-menu-item>
          <el-menu-item index="2-3">3</el-menu-item>
        </el-submenu>
        <el-submenu index="3">
          <template slot="title">Type</template>
          <el-menu-item index="3-1">1</el-menu-item>
          <el-menu-item index="3-2">2</el-menu-item>
          <el-menu-item index="3-3">3</el-menu-item>
        </el-submenu>
        <el-submenu index="4">
          <template slot="title">Region</template>
          <el-menu-item index="4-1">1</el-menu-item>
          <el-menu-item index="4-2">2</el-menu-item>
          <el-menu-item index="4-3">3</el-menu-item>
        </el-submenu>
        <el-submenu index="5">
          <template slot="title">Released year</template>
          <el-menu-item index="5-1">1</el-menu-item>
          <el-menu-item index="5-2">2</el-menu-item>
          <el-menu-item index="5-3">3</el-menu-item>
        </el-submenu>
      </el-menu>
      <el-container>
        <el-aside id="aside" width="300px">
          <div id="recommendedTitle">
            <span>Most popular movies</span>
          </div>
          <div class="mod_rank_list">
            <a href="#" class="rank_item" title="Tenet">
              <div class="num_and_title">
                <span id="first_rank" class="rank_num">1</span>
                <span class="rank_title">Frozen2</span>
              </div>
              <div class="rank_info">
                <div class="star">
                  <i class="el-icon-star-off"> 4.8</i>
                </div>
              </div>
            </a>
          </div>
          <div class="mod_rank_list">
            <a href="#" class="rank_item" title="Tenet">
              <div class="num_and_title">
                <span id="second_rank" class="rank_num">2</span>
                <span class="rank_title">The Boys</span>
              </div>
              <div class="rank_info">
                <div class="star">
                  <i class="el-icon-star-off"> 4.7</i>
                </div>
              </div>
            </a>
          </div>
          <div class="mod_rank_list">
            <a href="#" class="rank_item" title="Tenet">
              <div class="num_and_title">
                <span id="third_rank" class="rank_num">3</span>
                <span class="rank_title">Ironman</span>
              </div>
              <div class="rank_info">
                <div class="star">
                  <i class="el-icon-star-off"> 4.7</i>
                </div>
              </div>
            </a>
          </div>
          <div class="mod_rank_list">
            <a href="#" class="rank_item" title="Tenet">
              <div class="num_and_title">
                <span class="rank_num">4</span>
                <span class="rank_title">Spiderman</span>
              </div>
              <div class="rank_info">
                <div class="star">
                  <i class="el-icon-star-off"> 4.6</i>
                </div>
              </div>
            </a>
          </div>
          <div class="mod_rank_list">
            <a href="#" class="rank_item" title="Tenet">
              <div class="num_and_title">
                <span class="rank_num">5</span>
                <span class="rank_title">Tenet</span>
              </div>
              <div class="rank_info">
                <div class="star">
                  <i class="el-icon-star-off"> 4.6</i>
                </div>
              </div>
            </a>
          </div>
          <div class="mod_rank_list">
            <a href="#" class="rank_item" title="Tenet">
              <div class="num_and_title">
                <span class="rank_num">6</span>
                <span class="rank_title">Fargo</span>
              </div>
              <div class="rank_info">
                <div class="star">
                  <i class="el-icon-star-off"> 4.6</i>
                </div>
              </div>
            </a>
          </div>
          <div class="mod_rank_list">
            <a href="#" class="rank_item" title="Tenet">
              <div class="num_and_title">
                <span class="rank_num">7</span>
                <span class="rank_title">The Lie</span>
              </div>
              <div class="rank_info">
                <div class="star">
                  <i class="el-icon-star-off"> 4.6</i>
                </div>
              </div>
            </a>
          </div>
          <div class="mod_rank_list">
            <a href="#" class="rank_item" title="Tenet">
              <div class="num_and_title">
                <span class="rank_num">8</span>
                <span class="rank_title">Evil</span>
              </div>
              <div class="rank_info">
                <div class="star">
                  <i class="el-icon-star-off"> 4.5</i>
                </div>
              </div>
            </a>
          </div>
          <div class="mod_rank_list">
            <a href="#" class="rank_item" title="Tenet">
              <div class="num_and_title">
                <span class="rank_num">9</span>
                <span class="rank_title">Ratched</span>
              </div>
              <div class="rank_info">
                <div class="star">
                  <i class="el-icon-star-off"> 4.5</i>
                </div>
              </div>
            </a>
          </div>
        </el-aside>
        <el-main class="movieMain">
          <div class="movie">
            <el-card :body-style="{ padding: '0px' }">
              <img src="https://i.ebayimg.com/images/g/ycUAAOSwl-Fd1YZt/s-l640.jpg" class="image">
              <div style="padding: 14px;">
                <span>Spiderman</span>
                <div class="bottom clearfix">
                  <el-rate
                    v-model="value"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}">
                  </el-rate>
                  <el-button type="text" class="button">More info</el-button>
                </div>
              </div>
            </el-card>
          </div>
          <div class="movie">
            <el-card :body-style="{ padding: '0px' }">
              <img src="https://i0.wp.com/macguff.in/wp-content/uploads/2014/05/Amazing-Spider-Man-2-Movie-Poster.jpg?resize=400%2C600&ssl=1" class="image">
              <div style="padding: 14px;">
                <span>Spiderman</span>
                <div class="bottom clearfix">
                  <el-rate
                    v-model="value"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}">
                  </el-rate>
                  <el-button type="text" class="button">More info</el-button>
                </div>
              </div>
            </el-card>
          </div>
          <div class="movie">
            <el-card :body-style="{ padding: '0px' }">
              <img src="https://i0.wp.com/www.washtenawvoice.com/wp-content/uploads/2019/11/Jojo-rabbit-movie-poster.jpg?resize=400%2C600&ssl=1" class="image">
              <div style="padding: 14px;">
                <span>Jojo</span>
                <div class="bottom clearfix">
                  <el-rate
                    v-model="value"
                    disabled
                    show-score
                    text-color="#ff9900"
                    score-template="{value}">
                  </el-rate>
                  <el-button type="text" class="button">More info</el-button>
                </div>
              </div>
            </el-card>
          </div>
        </el-main>
      </el-container>
      <el-pagination
        background
        layout="prev, pager, next"
        :total="1000">
      </el-pagination>
    </el-main>
<!------------------------------ footer ------------------------------->
    <el-footer>
          <p id="copyright">&copy; 2020 copyright Filmfinder.com</p>
    </el-footer>
  </el-container>

</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<script>
export default {
  data() {
    return {
      input: ''
    }
  }
}
</script>

<script>
export default {
  data() {
    return {
      activeIndex: '1',
      activeIndex2: '1'
    };
  },
  methods: {
    handleSelect(key, keyPath) {
      console.log(key, keyPath);
    }
  }
}
</script>

<script>
export default {
  data() {
    return {
      currentDate: new Date()
    };
  }
}
</script>

<script>
export default {
  data() {
    return {
      value: 4.6
    }
  }
}
</script>

<script>
export default {
  data(){
      return{
        imagesBox:[{id:0,idView:require("../assets/1.jpg")},
          {id:1,idView:require("../assets/2.jpg")},
          {id:2,idView:require("../assets/3.jpg")},],
        fiveNews: []
      }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
html, body, #app{
  height: 100%;
}

.el-container{
  height: 100%;
}

.img{
  height: 400px;
  width: 800px;
}

.fixedHeader{
  position:fixed;
  z-index:1;
  top:0;
  width:100%;
  z-index:200;
}

.el-header{
  background-color: #dadbdb;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

#brandName{
  font-size: 36px;
  color: #03a032;
  font-weight: 600;
}

#searchBar{
  width: 350px;
  display: flex;
}

#searchButton{
  background-color: #03a032;
}

#infoMargin{
  margin-left: 20px;
}

.userInfo{
  font-size: 16px;
}

.el-main {
  background-color: #3f3f3f;
  padding: 0;
  width: 100%;
}

.el-carousel{
  margin-top: 80px;
  position: relative;
}

#showAside {
  background:rgba(0, 0, 0, 0.75);
  color: #333;
  position: absolute;top: 320px;
  height: 80px;
  z-index: 100;
}

.showDiv{
  float: left;
  text-align: justify;
  width: 70%;
  margin: 0 220px;
}

#showText{
  color: #ffffff;
  font-size: 16px;
}

.el-carousel__item h3 {
  color: #475669;
  font-size: 14px;
  opacity: 0.75;
  line-height: 200px;
  margin: 0;
}

.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}

.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}

.el-submenu{
  width: 20%;
}

.bottom {
  margin-top: 13px;
  line-height: 12px;
}

.button {
  padding: 0;
  float: center;
  font-size: 16px;
  margin-top: 15px;
}

.image {
  width: 100%;
  display: block;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both
}

#aside{
  background-color: #313136;
  color: #333;
  text-align: center;
  height:600px
}

#recommendedTitle{
  margin-top: 20px;
  font-size: 24px;
  font-weight: 600;
  color: #ffffff;
}

.rankList{
  color: #ffffff;
}

.mod_rank_list{
  display: flex;
  width: 200px;
  margin: 24px;
}

.rank_item{
  width: 350px;
}

.num_and_title{
  float: left;
}

#first_rank{
  color: #eec200;
}

#second_rank{
  color: #b4b4b1;
}

#third_rank{
  color: #a76c00;
}

.rank_num{
  font-size: 28px;
  margin-right: 10px;
  text-decoration: none;
  color: #c5c5c5;
  margin-left: 20px;
}

.rank_title{
  color: #ffffff;
}

.rank_info{
  float: right;
  margin-top: 7px;
}

.star{
  float: right;
}

.el-icon-star-off{
  color: #fffb02;
}

.movieMain{
  display: flex;
}

.el-pagination{
  margin: 30px 0;
}

.el-footer{
  background-color: #B3C0D1;
}

#copyright{
  float: right;
}

</style>
