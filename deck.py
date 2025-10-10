from collections import deque
import random

class DeckService:

    def shuffle(self, deck):
        # 預先洗牌
        deck = self.shuffle_and_cut(deck)
        # 攤牌洗牌
        deck = self.spread_shuffle(deck)
        # 將牌收攏
        deck = self.gather_deck(deck)
        # 切牌
        deck = self.split_and_merge(deck)
        # 逆時針調整牌的方向
        return self.turn_counterclockwise(deck)
    
    def draw_card(self, deck, count, random_pick=True):
        """
        從洗好的塔羅牌裡抽選，預設隨機
        """
        if random_pick:
            return random.sample(deck, count)
        else:
            return deck[:count]
         
    def shuffle_and_cut(self, deck):
        """
        Shuffle the deck of cards in place.
        """
        actions = ['shuffle', 'cut'] # 定義動作：洗牌或切牌
        times = random.randint(3, 5) # 隨機決定要做幾次動作

        random.shuffle(deck) # 先洗一次牌

        for _ in range(times):
            action = random.choice(actions) # 隨機決定要洗牌還是切牌
            if action == 'shuffle':
                random.shuffle(deck)
            elif action == 'cut':
                # 切牌位置 (避免太靠近兩端，這裡限制在 1/4 ~ 3/4 之間)
                cut_point = random.randint(len(deck)//4, len(deck)*3//4)
                # 切牌: 把上半段移到下半段之後
                deck = deck[cut_point:] + deck[:cut_point]

        return deck
    
    def spread_shuffle(self, deck):
        """
        模擬攤牌洗牌
        Args:
            deck (list): 牌堆
        Returns:
            list: 洗好的牌堆
        """
        direction = random.choice(["clockwise", "counterclockwise"]) # 順時鐘或逆時鐘
        rounds = random.randint(5, 10) # 要轉幾圈
       
        dq = deque(deck)
        
        for _ in range(rounds):

            # 每一圈隨機旋轉幾張方向
            steps = random.randint(len(deck)//3, len(deck)//2)
            for _ in range(steps):
                if direction == "clockwise":
                    dq.rotate(steps)   # 順時鐘
                else:
                    dq.rotate(-steps)  # 逆時鐘
    
                # 模擬攪動時會有些隨機亂數
                temp = list(dq) # 為處理先轉為 list
                random.shuffle(temp)
                

                # 模擬攪動時牌的方向會改變
                n = random.randint(3, len(temp)//2)  # 最少3張，最多整副牌的一半
                result = random.sample(range(0, len(temp)), n)
                for index in result:
                    temp[index]['position'] = self.__rotate_card(temp[index]['position'], direction)
                
                dq = deque(temp) # 處理完還原回 dq
    
        return list(dq)
    
    def __rotate_card(self, position, direction):
        """
        模擬塔羅牌方向變動
        """
        # clockwise	        順時針方向	（→ ↓ ← ↑）
        # counterclockwise	逆時針方向	 (← ↓ → ↑）
        clockwise = { "→":"↓", "↓":"←", "←":"↑", "↑":"→"}
        counterclockwise = { "←":"↓", "↓":"→", "→":"↑", "↑":"←"}

        choice =  clockwise if direction == 'clockwise' else counterclockwise

        return choice[position]

    def gather_deck(self, deck): 
        """
        把整副牌 deck 收攏
        模擬雙手在牌面上整理的狀態，先決定理牌的是左還是右手。
        如果使用左手往內收，朝上會變成向右，朝下會變成向左；反之亦然
        """
        lefthand = { "→":"→", "↑":"→", "←":"←", "↓":"←"}
        righthand = { "→":"→", "↑":"←", "←":"←", "↓":"→"}

        for card in deck:
            hand_map = random.choice([lefthand, righthand])
            card['position'] = hand_map[card['position']]
        return deck
    
    def split_and_merge(self, deck):
        """
        把整副牌 deck 分成三疊 (①, ②, ③)
        從第一疊抓取一部分 → 第二疊，再從第二疊抓取 → 形成第三疊。
        每疊至少保留 5 張。
        → 設定牌的順序 0 是最下面的一張
        """
        n = len(deck)
        min_size = (n // 5)   # 每疊最少要有的張數 (總牌數的 1/5)

        print(f"min_size={min_size}")

        # 從第一疊取出第二疊
        cut_1 = random.randint(min_size, n - 2 * min_size)  
        pile1 = deck[:cut_1]
        pile2 = deck[cut_1:]

        # 從第二疊取出第三疊
        cut_2 = random.randint(min_size, len(pile2) - min_size)
        pile3 = pile2[cut_2:]
        pile2 = pile2[:cut_2]

        return pile3 + pile2 + pile1
    
    def turn_counterclockwise(self, deck):
        """
        將整副牌逆時針轉向
        """
        counterclockwise = { "→":"↑", "←":"↓"}
        for card in deck:
            card['position'] = counterclockwise[card['position']]
        return deck