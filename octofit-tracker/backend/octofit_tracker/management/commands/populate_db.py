from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Delete all data
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')
        xmen = Team.objects.create(name='X-Men')
        justice = Team.objects.create(name='Justice League')
        avengers = Team.objects.create(name='Avengers')

        # Create users (5 per team)
        marvel_members = [
            User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel),
            User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel),
            User.objects.create(name='Natasha Romanoff', email='natasha@marvel.com', team=marvel),
            User.objects.create(name='Peter Parker', email='peter@marvel.com', team=marvel),
            User.objects.create(name='Wanda Maximoff', email='wanda@marvel.com', team=marvel),
        ]
        dc_members = [
            User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc),
            User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc),
            User.objects.create(name='Diana Prince', email='diana@dc.com', team=dc),
            User.objects.create(name='Barry Allen', email='barry@dc.com', team=dc),
            User.objects.create(name='Arthur Curry', email='arthur@dc.com', team=dc),
        ]
        xmen_members = [
            User.objects.create(name='Logan', email='logan@xmen.com', team=xmen),
            User.objects.create(name='Scott Summers', email='scott@xmen.com', team=xmen),
            User.objects.create(name='Jean Grey', email='jean@xmen.com', team=xmen),
            User.objects.create(name='Ororo Munroe', email='ororo@xmen.com', team=xmen),
            User.objects.create(name='Charles Xavier', email='charles@xmen.com', team=xmen),
        ]
        justice_members = [
            User.objects.create(name='Hal Jordan', email='hal@justice.com', team=justice),
            User.objects.create(name='John Stewart', email='john@justice.com', team=justice),
            User.objects.create(name='Shayera Hol', email='shayera@justice.com', team=justice),
            User.objects.create(name='Jonn Jonzz', email='jonn@justice.com', team=justice),
            User.objects.create(name='Wally West', email='wally@justice.com', team=justice),
        ]
        avengers_members = [
            User.objects.create(name='Thor Odinson', email='thor@avengers.com', team=avengers),
            User.objects.create(name='Bruce Banner', email='banner@avengers.com', team=avengers),
            User.objects.create(name='Clint Barton', email='clint@avengers.com', team=avengers),
            User.objects.create(name='Sam Wilson', email='sam@avengers.com', team=avengers),
            User.objects.create(name='Vision', email='vision@avengers.com', team=avengers),
        ]

        all_users = marvel_members + dc_members + xmen_members + justice_members + avengers_members

        # Create activities (10 total, 6 more)
        from random import choice, randint
        activity_types = ['Running', 'Cycling', 'Swimming', 'Yoga', 'Boxing', 'Climbing', 'Rowing', 'Dancing', 'Martial Arts', 'HIIT']
        for i in range(10):
            Activity.objects.create(
                user=choice(all_users),
                type=activity_types[i % len(activity_types)],
                duration=randint(15, 90),
                date=timezone.now()
            )

        # Create workouts
        w1 = Workout.objects.create(name='Super Strength', description='Strength training for heroes')
        w2 = Workout.objects.create(name='Flight Training', description='Aerobic and flight skills')
        w3 = Workout.objects.create(name='Mind Training', description='Mental focus and meditation')
        w1.suggested_for.set(marvel_members + avengers_members)
        w2.suggested_for.set(dc_members + justice_members)
        w3.suggested_for.set(xmen_members)

        # Create leaderboard with random points
        for team in [marvel, dc, xmen, justice, avengers]:
            Leaderboard.objects.create(team=team, points=randint(50, 200))

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data!'))
