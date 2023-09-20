from sts_support import *


class Card:
    """
    An abstract class from which all instantiable types of cards inheret.
    Provides the default card behaviour, which
    can be inhereted or overwritten by specific types of cards.
    The __init__ method for all cards do not take any
    arguments beyond self
    """

    def __init__(self):
        self._damage = 0
        self._block = 0
        self._cost = 1
        self._status = {}
        self._name = "Card"
        self._description = "A card."
        self._target = True

    def get_damage_amount(self) -> int:
        """
        Returns the amount of damage this card does to its target
        (i.e. the opponent it is played on).
        By default, the damage done by a card is 0.

        Returns:
            int: The amount of damage this card does to its target
        """
        return self._damage

    def get_block(self) -> int:
        """
        Returns the amount of block this card adds to its user.
        By default, the block amount provided by a card is
        0.

        Returns:
            int: The amount of block this card adds to its user.
        """
        return self._block

    def get_energy_cost(self) -> int:
        """
        Returns the amount of energy this card costs to play.
        By default, the energy cost should be 1.

        Returns:
            int: The amount of energy this card costs to play
        """
        return self._cost

    def get_status_modifiers(self) -> dict[str, int]:
        """
        Returns a dictionary describing each status modifiers applied when this card is played.
        By default, no status modifiers are applied;
        that is, this method should return an empty dictionary in the abstract Card class.

        Returns:
            dict[str, int]: A dictionary describing each status modifiers
            applied when this card is played
        """
        return self._status

    def get_name(self) -> str:
        """
        Returns the name of the card. In the Card superclass, this is just the string ‘Card’.

        Returns:
            str: The name of the card.
        """
        return self._name

    def get_description(self) -> str:
        """
        Returns a description of the card.
        In the Card superclass, this is just the string ‘A card.’.

        Returns:
            str: A description of the card.
        """
        return self._description

    def requires_target(self) -> bool:
        """
        Returns True if playing this card requires a target, and False if it does not.
        By default, a card does require a target.

        Returns:
            bool: If playing this card requires a target.
        """
        return self._target

    def __str__(self) -> str:
        """
        Returns the string representation for the card,
        in the format ‘{Card name}: {Card description}’.

        Returns:
            str: The string representation for the card.
        """
        return f"{self._name}: {self._description}"

    def __repr__(self) -> str:
        """
        Returns the text that would be required to create a new instance of this class
        identical to self.

        Returns:
            str: The text that would be required to create a new instance of this class
        """
        return self.__class__.__name__ + "()"


class Strike(Card):
    """
    Inherits from Card

    Strike is a type of Card that deals 6 damage to its target. It costs 1 energy point to play
    """

    def __init__(self):
        super().__init__()
        self._damage = 6
        self._cost = 1
        self._name = "Strike"
        self._description = "Deal 6 damage."
        self._target = True


class Defend(Card):
    """
    Inherits from Card

    Defend is a type of Card that adds 5 block to its user.
    Defend does not require a target. It costs 1 energy point to play.
    """

    def __init__(self):
        super().__init__()
        self._block = 5
        self._cost = 1
        self._name = "Defend"
        self._description = "Gain 5 block."
        self._target = False


class Bash(Card):
    """
    Inherits from Card

    Bash is a type of Card that adds 5 block to its user and causes 7 damage to its target.
    It costs 2 energy points to play.
    """

    def __init__(self):
        super().__init__()
        self._damage = 7
        self._block = 5
        self._cost = 2
        self._name = "Bash"
        self._description = "Deal 7 damage. Gain 5 block."
        self._target = True


class Neutralize(Card):
    """
    Inherits from Card

    Neutralize is a type of card that deals 3 damage to its target.
    It also applies status modifiers to its target;
    namely, it applies 1 weak and 2 vulnerable.
    Neutralize does not cost any energy points to play
    """

    def __init__(self):
        super().__init__()
        self._damage = 3
        self._cost = 0
        self._status = {"weak": 1, "vulnerable": 2}
        self._name = "Neutralize"
        self._description = "Deal 3 damage. Apply 1 weak. Apply 2 vulnerable."
        self._target = True


class Survivor(Card):
    """
    Inherits from Card

    Survivor is a type of card that adds 8 block and applies 1 strength to its user.
    Survivor does not require a target.
    """

    def __init__(self):
        super().__init__()
        self._block = 8
        self._status = {"strength": 1}
        self._name = "Survivor"
        self._description = "Gain 8 block and 1 strength."
        self._target = False


class Entity:
    """
    Represents an entity in the game, such as a player or a monster.

    Attributes:
    -hp (int): The health points of the entity.
            Starts at the maximum HP for the entity,
            and may decrease over the course of one or more encounters.
            An entity is defeated when its HP is reduced to 0.

    -block (int): The amount of defense the entity has.
                When an entity is attacked, damage is applied to the block first.
                Only once the block has been reduced to 0,
                will any remaining damage be caused to the entity's HP.

    -strength (int): The amount of additional strength this entity has.
                    When an entity plays a card that causes damage to a target,
                    the damage caused will increase by 1 for each strength point the entity has.
                    Strength does not wear off until the end of an encounter.

    -weak (int): The number of turns for which this entity is weak.
                If an entity is weak on a given turn,
                all cards played by the entity that cause damage will cause 25% less damage.

    -vulnerable (int): The number of turns for which this entity is vulnerable.
                    If an entity is vulnerable on a turn,
                    damage caused to it will be increased by 50%.
    """

    def __init__(self, max_hp: int) -> None:
        """
        Set up a new entity with the given max_hp.

        An entity starts with the maximum amount of HP it can have. Block, strength,
        weak, and vulnerable all start at 0.

        Args:
            max_hp (int): The maximum amount of health points the entity can have.

        Returns:
            None: This method does not return anything.
        """
        self._max_hp = max_hp
        self._hp = max_hp
        self._block = 0
        self._strength = 0
        self._weak = 0
        self._vulnerable = 0
        self._name = self.__class__.__name__

    def get_hp(self) -> int:
        """
        Returns the current HP for this entity.

        Returns:
            int: The current HP for this entity.
        """
        return self._hp

    def get_max_hp(self) -> int:
        """
        Returns the maximum possible HP for this entity.

        Returns:
            int: The maximum possible HP for this entity.
        """
        return self._max_hp

    def get_block(self) -> int:
        """
        Returns the amount of block for this entity.

        Returns:
            int: The amount of block for this entity.
        """
        return self._block

    def get_strength(self) -> int:
        """
        Returns the amount of strength for this entity.

        Returns:
            int: The amount of strength for this entity.
        """
        return self._strength

    def get_weak(self) -> int:
        """
        Returns the number of turns for which this entity is weak.

        Returns:
            int: The number of turns for which this entity is weak.
        """
        return self._weak

    def get_vulnerable(self) -> int:
        """
        Returns the number of turns for which this entity is vulnerable.

        Returns:
            int: The number of turns for which this entity is vulnerable.
        """
        return self._vulnerable

    def get_name(self) -> str:
        """
        Returns the name of the entity.
        The name of an entity is just the name of the most specific class it belongs to.

        Returns:
            str: The name of the entity.
        """
        return self._name

    def reduce_hp(self, amount: int) -> None:
        """
        Attacks the entity with a damage of amount.
        This involves reducing block until the amount of damage has
        been done or until block has reduced to zero,
        in which case the HP is reduced by the remaining amount.
        For example, if an entity has 20 HP and 5 block,
        calling reduce_hp with an amount of 10 would result in 15 HP and 0 block.
        HP cannot go below 0.

        Parameters:
            int: Attacks the entity with a damage of amount.

        Returns:
            None
        """
        # If the amount is completely covered by the block, subtract it from block
        if self._block >= amount:
            self._block -= amount
        else:
            # Else, subtract the blocked amount to find the new amount to be subtracted from hp
            amount -= self._block
            # Generate new hp value after subtracting non blocked amount
            self._hp -= amount
            self._block = 0
            # Ensures hp stays above 0
            self._hp = max(self._hp, 0)

    def is_defeated(self) -> bool:
        """
        Returns True if the entity is defeated, and False otherwise.
        An entity is defeated if it has no HP remaining.

        Returns:
            bool: True if the entity is defeated, and False otherwise.
        """
        # Returns false if the entity has hp remaining (alive), otherwise returns True
        if self._hp > 0:
            return False
        if self._hp == 0:
            return True

    def add_block(self, amount: int) -> None:
        """
        Adds the given amount to the amount of block this entity has.

        Parameters:
            int: given amount to be added to block

        Returns:
            None
        """
        self._block += amount

    def add_strength(self, amount: int) -> None:
        """
        Adds the given amount to the amount of strength this entity has.

        Parameters:
            int: given amount to be added to strength

        Returns:
            None
        """
        self._strength += amount

    def add_weak(self, amount: int) -> None:
        """
        Adds the given amount to the amount of weak this entity has.

        Parameters:
            int: given amount to be added to weak

        Returns:
            None
        """
        self._weak += amount

    def add_vulnerable(self, amount: int) -> None:
        """
        Adds the given amount to the amount of vulnerable this entity has.

        Paramters:
            int: given amount to be added to vulnerable

        Returns:
            None
        """
        self._vulnerable += amount

    def new_turn(self) -> None:
        """
        Applies any status changes that occur when a new turn begins.
        For the base Entity class, this involves setting
        block back to 0, and reducing weak and vulnerable each by 1 if they are greater than 0.

        Returns:
            None
        """
        self._block = 0
        self._weak -= 1
        self._weak = max(self._weak, 0)  # Ensures weak does not become negative
        self._vulnerable -= 1
        self._vulnerable = max(
            self._vulnerable, 0
        )  # Ensures vulnerable does not become negative

    def __str__(self) -> str:
        """
        Returns the string representation for the entity in the format
        ‘{entity name}: {current HP}/{max HP} HP’.

        Returns:
            str: String representation for the entity
        """
        return f"{self._name}: {self._hp}/{self._max_hp} HP"

    def __repr__(self) -> str:
        """
        Returns the text that would be required to create a new instance of this class
        identical to self.

        Returns:
            str: The text that would be required to create a new instance of this class
        """
        return self.__class__.__name__ + f"({self._max_hp})"


class Player(Entity):
    """
    An abstract class representing a type of entity that the user controls.

    Inherits from Entity and defines additional functionality specific to a Player,
    including energy and cards.

    Attributes:
    - energy (int): The amount of energy the player has available to use each turn.

    - deck (list): A list of cards remaining to be drawn from the player's deck.

    - hand (list): A list of cards playable in the current turn.

    - discard_pile (list): A list of cards that have been played already this encounter.
    """

    def __init__(self, max_hp: int, cards: list[Card] | None = None) -> None:
        """
        Initializes a Player object with a maximum health points (max_hp)
        and a list of cards (cards).

        Args:
        max_hp (int): the maximum health points for the player.

        cards (list[Card] | None, optional):
        a list of Card objects representing the player's deck. Defaults to None.

        Returns:
        None

        Notes:
        This method initializes the Player's energy to 3 and three lists of cards
        (deck, hand, and discard pile).
        If cards is not None, the deck is initialized to be the cards parameter,
        otherwise, it is initialized as an empty list.
        The player's hand and discard piles start as empty lists.
        """
        super().__init__(max_hp)
        self._cards = cards
        self._energy = 3
        self._deck = self._cards
        self._hand = []
        self._discard = []

    def get_energy(self) -> int:
        """
        Returns the amount of energy the user has remaining.

        Returns:
            int: the amount of energy remaining.
        """
        return self._energy

    def get_hand(self) -> list[Card]:
        """
        Returns the players current hand.

        Returns:
            list: The players current hand.
        """
        return self._hand

    def get_deck(self) -> list[Card]:
        """
        Returns the players current deck.

        Returns:
            list: The players current deck.
        """
        return self._deck

    def get_discarded(self) -> list[Card]:
        """
        Returns the players current discard pile.

        Returns:
            list: the players current discard pile.
        """
        return self._discard

    def start_new_encounter(self) -> None:
        """
        Adds all cards from the player’s discard pile to the end of their deck,
        and sets the discard pile to be an empty list.
        Pre-condition: The player’s hand should be empty when this method is called.
        """
        if self._hand == []:
            self._deck.extend(self._discard)
            self._discard = []

    def end_turn(self) -> None:
        """
        This method adds all remaining cards from the player’s hand
        to the end of their discard pile, and sets their hand back to an empty list.
        """
        self._discard.extend(self._hand)
        self._hand = []

    def new_turn(self) -> None:
        """
        This method sets the player up for a new turn.
        This involves everything that a regular entity requires for a new turn,
        but also requires that the player be dealt a new hand of 5 cards, and energy be reset to 3.
        """
        self._energy = 3
        draw_cards(self._deck, self._hand, self._discard)
        super().new_turn()

    def play_card(self, card_name: str) -> Card | None:
        """
        Attempts to play a card from the player's hand.
        If a card with the given name exists in the player's hand and
        the player has enough energy to play said card,
        the card is removed from the player's hand and added to the discard pile,
        the required energy is deducted from the player's energy, and the card is returned.
        If no card with the given name exists in the player's hand,
        or the player doesn't have enough energy to play the requested card,
        this function returns None.

        Args:
            card_name (str): The name of the card to be played.

        Returns:
            Card or None: If successful, returns the played Card object. Otherwise, returns None.
        """
        # check if the player has the card in their hand
        for index, card in enumerate(self._hand):
            if card.get_name() == card_name:
                # check if the player has enough energy to play the card
                if self._energy >= card.get_energy_cost():
                    # remove the card from the player's hand
                    card_played = self._hand.pop(index)
                    # add the card to the discard pile
                    self._discard.append(card_played)
                    # deduct the required energy from the player's energy
                    self._energy -= card_played.get_energy_cost()
                    return card_played
        return None  # card not found in the player's hand

    def __repr__(self) -> str:
        """
        Returns the text that would be required to create a new instance of this class
        identical to self.

        Returns:
            str: The text that would be required to create a new instance of this class
        """
        return self.__class__.__name__ + f"({self._max_hp}, {self._cards})"


class IronClad(Player):
    """
    A type of player that starts with 80 HP and a specific deck composition.

    Inherits from Player.

    Attributes:
    - hp (int): the current hit points of the player
    - max_hp (int): the maximum hit points of the player
    - deck (list of Card): the player's deck of cards
    - discard_pile (list of Card): the player's discard pile of cards
    - draw_pile (list of Card): the player's draw pile of cards

    The IronClad's deck contains 5 Strike cards, 4 Defend cards, and 1 Bash card.
    """

    def __init__(self) -> None:
        super().__init__(80)
        self._deck = [
            Strike(),
            Strike(),
            Strike(),
            Strike(),
            Strike(),
            Defend(),
            Defend(),
            Defend(),
            Defend(),
            Bash(),
        ]

    def __repr__(self) -> str:
        """
        Returns the text that would be required to create a new instance of this class
        identical to self.

        Returns:
            str: The text that would be required to create a new instance of this class
        """
        return self.__class__.__name__ + "()"


class Silent(Player):
    """
    A type of player that starts with 70 HP and has a unique deck composition.
    Inherits from the Player class.

    Attributes:
    - hp (int): the current hit points of the player
    - max_hp (int): the maximum hit points of the player
    - deck (list of Card): the player's deck of cards
    - discard_pile (list of Card): the player's discard pile of cards
    - draw_pile (list of Card): the player's draw pile of cards

    Silent’s deck contains 5 Strike cards, 5 Defend cards, 1 Neutralize card, and 1 Survivor card.
    """

    def __init__(self) -> None:
        super().__init__(70)
        self._deck = [
            Strike(),
            Strike(),
            Strike(),
            Strike(),
            Strike(),
            Defend(),
            Defend(),
            Defend(),
            Defend(),
            Defend(),
            Neutralize(),
            Survivor(),
        ]

    def __repr__(self) -> str:
        """
        Returns the text that would be required to create a new instance of this class
        identical to self.

        Returns:
            str: The text that would be required to create a new instance of this class
        """
        return self.__class__.__name__ + "()"


class Monster(Entity):
    """
    Abstract class that represents a type of entity that the user battles during encounters.

    Inherits from Entity, and in addition to regular entity functionality,
    each monster has a unique id,
    and an action method that handles the effects of the monster’s action on
    itself, and describes the effect the monster’s action would have on its target.

    Attributes:
    - id (int): A unique identifier for the monster.
    """

    monster_count = 0

    def __init__(self, max_hp: int) -> None:
        """
        Initializes a new instance of the Monster class
        with the given maximum HP and a unique ID number.

        Args:
            max_hp (int): The maximum HP of the monster.

        Returns:
            None
        """
        super().__init__(max_hp)
        self._id = Monster.monster_count
        Monster.monster_count += 1

    def get_id(self) -> int:
        """
        Returns the unique id number of this monster.

        Returns:
            int: Unique id number of the monster.
        """
        return self._id

    def action(self) -> dict[str, int]:
        """
        Performs the current action for this monster
        and returns a dictionary describing the effects this monster's
        action should cause to its target.
        In the abstract Monster superclass, this method should just raise a NotImplementedError.
        This method must be overwritten by the instantiable subclasses of Monster, with the
        strategies specific to each type of monster.

        Returns:
            dict[str, int]:
            A dictionary describing the effects this monster's action should cause to its target.
        """
        raise NotImplementedError()


class Louse(Monster):
    """
    This class inherits from the Monster class and
    overrides the action method to return a dictionary
    containing the amount of damage the Louse monster can inflict on its target.
    The amount of damage is randomly generated between 5 and 7 (inclusive)
    when the Louse instance is created.
    """

    def __init__(self, max_hp: int) -> None:
        """
        Initializes a new instance of the Louse class
        with the given maximum HP

        Args:
            max_hp (int): The maximum HP of the monster.

        Returns:
            None
        """
        super().__init__(max_hp)
        self._damage_amount = random_louse_amount()

    def action(self) -> dict[str, int]:
        """
        Performs the current action for this Louse
        and returns a dictionary describing the effects this monster's
        action should cause to its target.

        Returns:
            dict[str, int]:
            A dictionary describing the effects this monster's action should cause to its target.
        """
        return {"damage": self._damage_amount}


class Cultist(Monster):
    """
    A subclass of Monster representing a Cultist.

    Inherits from Monster class and has an action method that
    returns a dictionary containing the damage and weak values.
    """

    def __init__(self, max_hp: int) -> None:
        """
        Initializes a new instance of the Cultist class
        with the given maximum HP

        Args:
            max_hp (int): The maximum HP of the monster.

        Returns:
            None
        """
        super().__init__(max_hp)
        self._num_calls = 0
        self._damage_amount = 0
        self._weak_amount = 0

    def action(self) -> dict[str, int]:
        """
        Returns a dictionary containing the damage and weak values for a specific Cultist instance.

        For each Cultist instance, damage_amount is 0 the first time action is called.
        For each subsequent call to action,
        damage_amount = 6 + num_calls, where num_calls is the number of times
        the action method has been called on this specific Cultist instance.
        The weak_amount alternates between 0 and 1
        each time the action method is called on a specific Cultist instance,
        starting at 0 for the first call.

        Returns:

            A dictionary containing the damage and weak values.
            {
                'damage': damage_amount,
                'weak': weak_amount
            }
        """
        # set damage to 0 if action has not been called
        if self._num_calls == 0:
            self._damage_amount = 0
        # calculate new damage amount using number of times action has been called
        else:
            self._damage_amount = self._num_calls + 6
        # set weak amount to alternate between 0 and 1
        self._weak_amount = self._num_calls % 2
        # update the number of times action has been called
        self._num_calls += 1
        return {"damage": self._damage_amount, "weak": self._weak_amount}


class JawWorm(Monster):
    """
    A class representing a monster called JawWorm, which inherits from the Monster class.
    """

    def __init__(self, max_hp: int) -> None:
        """
        Initializes a new instance of the JawWorm class
        with the given maximum HP

        Args:
            max_hp (int): The maximum HP of the monster.

        Returns:
            None
        """
        super().__init__(max_hp)
        self._damage_taken = 0
        self._damage_amount = 0

    def action(self) -> dict[str, int]:
        """
        Each time action is called on a JawWorm instance, the following effects occur:
        - Half of the amount of damage the jaw worm has taken so far (rounding up)
        is added to the jaw worm's own block amount.
        - Half of the amount of damage the jaw worm has taken so far (rounding down)
        is used for damage to the target.

        The amount of damage taken so far is the difference
        between the jaw worm's maximum HP and its current HP.

        Returns:
            dict[str, int]:
            A dictionary describing the effects this monster's action should cause to its target.
        """
        self._damage_taken = self._max_hp - self._hp
        # round up for block amount
        self._block = (self._damage_taken + 1) // 2
        # round down for damage taken
        self._damage_amount = self._damage_taken // 2
        return {"damage": self._damage_amount}


class Encounter:
    """
    Each encounter in the game is represented as an instance of the Encounter class.
    This class manages one player and a set of 1 to 3 monsters,
    and facilitates the interactions between the player and monsters.
    """

    def __init__(self, player: Player, monsters: list[tuple[str, int]]) -> None:
        """
        Initializes a new encounter for the player with a list of monsters.

        Args:
            player (Player): The instance of the player participating in the encounter.
            monsters (list[tuple[str, int]]):
            A list of tuples describing the monsters in the encounter. Each tuple contains
            the name (type) of the monster and the monster's max HP.

        Returns:
            None
        """
        self._player = player
        self._monsters = []
        # iterate over monsters to create the required monster instances
        for monster_type, max_hp in monsters:
            if monster_type == "Louse":
                self._monsters.append(Louse(max_hp))
            elif monster_type == "Cultist":
                self._monsters.append(Cultist(max_hp))
            elif monster_type == "JawWorm":
                self._monsters.append(JawWorm(max_hp))
        self._player.start_new_encounter()
        self._player_turn = True
        self._player.new_turn()

    def start_new_turn(self) -> None:
        """
        This method sets it to be the player’s turn
        (i.e. the player is permitted to attempt to apply cards) and called
        new_turn on the player instance.
        """
        self._player_turn = True
        self._player.new_turn()

    def end_player_turn(self) -> None:
        """
        This method sets it to not be the player’s turn
        (i.e. the player is not permitted to attempt to apply cards),
        and ensures all cards remaining in the player’s hand move into their discard pile.
        This method also calls the
        new_turn method on all monster instances remaining in the encounter.
        """
        self._player_turn = False
        self._player.end_turn()
        # start a new turn for each monster
        for monster in self._monsters:
            monster.new_turn()

    def get_player(self) -> Player:
        """
        Returns the player in this encounter.

        Returns:
            Player: the player in this encounter
        """
        return self._player

    def get_monsters(self) -> list[Monster]:
        """
        Returns a list of Monster objects representing the monsters remaining in this encounter.

        Returns:
            list[Monster]:
            A list of Monster objects representing the monsters remaining in this encounter.
        """
        remaining_monsters = []

        # iterate over monsters to check defeated status
        for monster in self._monsters:
            if monster.is_defeated() is False:
                remaining_monsters.append(monster)
        return remaining_monsters

    def is_active(self) -> bool:
        """
        Returns True if there are monsters remaining in this encounter, and False otherwise.

        Returns:
            bool: True if there are monsters remaining in this encounter, and False otherwise
        """
        for monster in self._monsters:
            if monster.is_defeated() is False:
                return True
        return False

    def player_apply_card(self, card_name: str, target_id: int | None = None) -> bool:
        """
        This method attempts to apply the first card with the given name from the player's hand.
        If the card requires a target, the target is specified by the given target_id.
        The steps executed by this method are as follows:

        1. Return False if the application of the card is invalid for any of the following reasons:
            - If it is not the player's turn.
            - If the card with the given name requires a target but no target was given.
            - If a target was given but no monster remains in this encounter with that id.

        2. The player attempts to play a card with the given name.
        If this is not successful (i.e. the card did not exist in the
        player's hand, the player didn't have enough energy,
        or the card name doesn't map to a card),
        this function returns False.
        Otherwise, the function should execute the remaining steps.

        3. Any block and strength from the card should be added to the player.

        4. If a target was specified:
            (a) Any vulnerable and weak from the card should be applied to the target.
            (b) Damage is calculated and applied to the target.
            The base damage is the amount of damage caused by the card, plus
            the strength of the player.
            If the target is vulnerable (i.e. their vulnerable stat is non-zero)
            the damage should be multiplied by 1.5 and if the player is weak
            (i.e. their weak stat is non-zero) it should be multiplied by 0.75.
            The damage amount should be converted to an int before being applied to the target.
            Int conversions should round down
            (note that this is the default behaviour of type casting to an int).
            (c) If the target has been defeated, remove them from the list of monsters.

        5. Return True to indicate that the function executed successfully.

        Parameters:
            str(card_name): A string representing the name of the card to be applied.
            int(target_id): An optional integer representing the id of the target monster
            (if the card requires a target).

        Returns:
            bool: A boolean value indicating
            whether the application of the card was successful or no

        """
        # Step 1: check if the card application is invalid for any reason
        if self._player.get_energy() <= 0:
            return False

        if not self._player_turn:
            return False

        if card_name not in ("Strike", "Defend", "Bash", "Neutralize", "Survivor"):
            return False

        if card_name in ("Strike", "Bash", "Neutralize") and target_id is None:
            return False

        monster_ids = []
        for monster in self._monsters:
            monster_ids.append(monster.get_id())
        if target_id is not None and target_id not in monster_ids:
            return False

        # Step 2: attempt to play the card, if played store it in a variable
        card = self._player.play_card(card_name)

        if card is None:
            return False

        # Step 3: add any block and strength from the card to the player
        self._player.add_block(card.get_block())
        if "strength" in card.get_status_modifiers():
            self._player.add_strength(card.get_status_modifiers()["strength"])

        # Step 4: if a target was specified, apply vulnerable and weak, calculate and apply damage
        for monster in self._monsters:
            if monster.get_id() == target_id:
                target = monster
                if "vulnerable" in card.get_status_modifiers():
                    target.add_vulnerable(card.get_status_modifiers()["vulnerable"])
                if "weak" in card.get_status_modifiers():
                    target.add_weak(card.get_status_modifiers()["weak"])

                damage = card.get_damage_amount() + self._player.get_strength()
                if target.get_vulnerable() > 0:
                    damage *= 1.5
                if self._player.get_weak() > 0:
                    damage *= 0.75

                damage = int(damage)
                target.reduce_hp(damage)
                if target.is_defeated() is True:
                    self._monsters.remove(target)

        # Step 5: return True to indicate success
        return True

    def enemy_turn(self) -> None:
        """
        Attempts to allow all remaining monsters in the encounter to take an action.
        If it is the player’s turn,
        returns immediately. Otherwise, each monster takes a turn (in order) as follows:
        1. The monster attempts its action (see the action method in the Monster class).
        2. Any weak and vulnerable generated by the monster’s action are added to the player.
        3. Any strength generated by the monster’s action are added to the monster.
        4. Damage is calculated and applied to the target.
        The base damage is the amount of damage caused by
        the monster’s action, plus the strength of the monster.
        If the player is vulnerable the damage should be
        multiplied by 1.5 and if the monster is weak it should be multiplied by 0.75.
        The damage amount should be converted to an int before being applied to the player.
        Once all monster’s have played an action, this method starts a new turn.

        Returns:
            None
        """
        # Check if it's the player's turn
        if self._player_turn is True:
            return

        # Iterate over monsters
        for monster in self._monsters:
            action = monster.action()

            # Add weak and vulnerable to player
            if "weak" in action:
                self._player.add_weak(action["weak"])
            if "vulnerable" in action:
                self._player.add_vulnerable(action["vulnerable"])

            # Add strength to monster
            if "strength" in action:
                monster.add_strength(action["strength"])

            # Damage calculation and application
            damage = +monster.get_strength() + action["damage"]
            if self._player.get_vulnerable() > 0:
                damage *= 1.5
            if monster.get_weak() > 0:
                damage *= 0.75
            damage = int(damage)
            self._player.reduce_hp(damage)

        # Start a new turn
        self.start_new_turn()


def main():
    """
    This function prompts the user to select a type of player ('ironclad' or 'silent')
    and creates the relevant player instance.
     Then, it prompts the user for a game file, reads it with the help of a
    function from sts_support.py, and starts an encounter
    with the set of monsters described in the file.
    For each encounter,
    the function prompts the user for moves, based on Table 1.
    If the player wins the encounter, their turn is ended before starting the next encounter.
    If the player defeats all encounters,
    the function terminates with a game win message.
    If the player is defeated after the enemy turn, the
    game terminates with a game lose message.

    Move name           Behaviour
    'end turn'          Ends the player's turn and starts the enemy turn.
                        If the player is defeated after
                        the enemy turn, the game terminates with the game lose message.
                        Otherwise, the
                        resulting encounter state is displayed.
    'inspect {deck |    When the user enters 'inspect deck',
                        the player's deck is printed. When the user
    discard}'           enters 'inspect discard', the player's discard pile is printed.

    'describe {card_name}' When the user enters this command,
                        the description for the card with the given
                        card_name is printed.
                        If the player does not have an instance of the requested
                        card, its description is still printed.

    'play {card_name}'   Attempts to play a card with the given card_name.
                        If the card application fails for any reason,
                        the card failure message is printed. Otherwise, the resulting
                        encounter state is printed.
                        If the user enters 'play {card_name} {target_id}',
                        the card is played on the monster with the specified target_id,
                        if it exists in the encounter.
                         Otherwise, an error message is printed.
    """
    # Implement this only once you've finished and tested ALL of the required
    # classes.

    # ask for player type and store as variable
    player_type = input("Enter a player type: ")
    if player_type == "ironclad":
        player = IronClad()
    elif player_type == "silent":
        player = Silent()

    # ask for file and store as variable
    filename = input("Enter a game file: ")
    game_data = read_game_file(filename)

    # iterate over data in game file to create encounters
    for monster_data in game_data:
        encounter = Encounter(player, monster_data)
        print("New encounter!\n")
        display_encounter(encounter)

        # while the encounter is active implement the moves and their behaviours
        while encounter.is_active() is True:
            move_name = input("Enter a move: ")

            if move_name == "end turn":
                encounter.end_player_turn()
                encounter.enemy_turn()
                if player.is_defeated() is False:
                    display_encounter(encounter)
                # check if player has lost
                elif player.is_defeated() is True:
                    print(GAME_LOSE_MESSAGE)
                    return

            elif move_name == "inspect deck":
                print(f"\n{encounter.get_player().get_deck()}\n")

            elif move_name == "inspect discard":
                print(f"\n{encounter.get_player().get_discarded()}\n")

            elif move_name == "describe Strike":
                print(f"\n{Strike().get_description()}\n")

            elif move_name == "describe Defend":
                print(f"\n{Defend().get_description()}\n")

            elif move_name == "describe Bash":
                print(f"\n{Bash().get_description()}\n")

            elif move_name == "describe Neutralize":
                print(f"\n{Neutralize().get_description()}\n")

            elif move_name == "describe Survivor":
                print(f"\n{Survivor().get_description()}\n")

            elif move_name[0:4] == "play":
                list_of_words = move_name.split()

                if len(list_of_words) == 2:
                    card_name = list_of_words[1]
                    apply_card_result = encounter.player_apply_card(card_name)

                elif len(list_of_words) == 3:
                    card_name = list_of_words[1]
                    target_id = int(list_of_words[2])
                    apply_card_result = encounter.player_apply_card(
                        card_name, target_id
                    )

                if apply_card_result is False:
                    print(CARD_FAILURE_MESSAGE)

                elif apply_card_result is True:
                    display_encounter(encounter)

        # check if player has won encounter
        if (
            encounter.is_active() is False
            and encounter.get_player().is_defeated() is False
        ):
            encounter.get_player().end_turn()
            print(f"{ENCOUNTER_WIN_MESSAGE}")

    # if player completes all encounters print win message and end the game
    print(GAME_WIN_MESSAGE)
    return


if __name__ == "__main__":
    main()
