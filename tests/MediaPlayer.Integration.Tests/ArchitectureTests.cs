using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Xml.Linq;
using Xunit;

namespace MediaPlayer.Integration.Tests;

/// <summary>
/// Enforces the project dependency direction documented in docs/architecture/README.md.
/// These tests read project files only. They do not load production code.
/// </summary>
[Trait("Category", "Architecture")]
public sealed class ArchitectureTests
{
    private const string SOLUTION_FILE_NAME = "MediaPlayer.slnx";

    private static readonly Dictionary<string, string[]> _allowedProjectReferences = new(StringComparer.Ordinal)
    {
        ["MediaPlayer.Core"] = [],
        ["MediaPlayer.Application"] = ["MediaPlayer.Core"],
        ["MediaPlayer.Playback.LibVLC"] = ["MediaPlayer.Application"],
        ["MediaPlayer.Infrastructure"] = ["MediaPlayer.Application"],
        ["MediaPlayer.Desktop"] = ["MediaPlayer.Application", "MediaPlayer.Infrastructure", "MediaPlayer.Playback.LibVLC"],
    };

    private static readonly string[] _uiAndNativePackagePrefixes = ["Avalonia", "LibVLCSharp", "VideoLAN."];

    /// <summary>
    /// Every production project exists and has a documented dependency rule.
    /// </summary>
    [Fact]
    public void SourceProjects_MatchDocumentedModules()
    {
        string[] actual = [.. Directory.GetFiles(Path.Combine(FindRepositoryRoot(), "src"), "*.csproj", SearchOption.AllDirectories)
            .Select(path => Path.GetFileNameWithoutExtension(path))
            .Order(StringComparer.Ordinal)];

        Assert.Equal(_allowedProjectReferences.Keys.Order(StringComparer.Ordinal), actual);
    }

    /// <summary>
    /// Production projects reference only the projects that the dependency direction allows.
    /// </summary>
    /// <param name="projectName">The production project name.</param>
    [Theory]
    [InlineData("MediaPlayer.Core")]
    [InlineData("MediaPlayer.Application")]
    [InlineData("MediaPlayer.Playback.LibVLC")]
    [InlineData("MediaPlayer.Infrastructure")]
    [InlineData("MediaPlayer.Desktop")]
    public void SourceProject_ReferencesOnlyAllowedProjects(string projectName)
    {
        string[] references = [.. LoadProject(projectName).Descendants("ProjectReference")
            .Select(element => Path.GetFileNameWithoutExtension(((string?)element.Attribute("Include") ?? string.Empty).Replace('\\', '/')))
            .Order(StringComparer.Ordinal)];

        Assert.Equal(_allowedProjectReferences[projectName].Order(StringComparer.Ordinal), references);
    }

    /// <summary>
    /// Core and Application stay free of UI and native playback packages.
    /// </summary>
    /// <param name="projectName">The production project name.</param>
    [Theory]
    [InlineData("MediaPlayer.Core")]
    [InlineData("MediaPlayer.Application")]
    public void InnerProject_HasNoUiOrNativePlaybackPackages(string projectName)
    {
        IEnumerable<string> packages = LoadProject(projectName).Descendants("PackageReference")
            .Select(element => (string?)element.Attribute("Include") ?? string.Empty);

        Assert.DoesNotContain(packages, package => _uiAndNativePackagePrefixes.Any(prefix => package.StartsWith(prefix, StringComparison.OrdinalIgnoreCase)));
    }

    private static XDocument LoadProject(string projectName)
    {
        string path = Path.Combine(FindRepositoryRoot(), "src", projectName, projectName + ".csproj");
        return XDocument.Load(path);
    }

    private static string FindRepositoryRoot()
    {
        DirectoryInfo? directory = new(AppContext.BaseDirectory);
        while (directory is not null && !File.Exists(Path.Combine(directory.FullName, SOLUTION_FILE_NAME)))
        {
            directory = directory.Parent;
        }

        return directory?.FullName ?? throw new DirectoryNotFoundException("Could not find " + SOLUTION_FILE_NAME + ".");
    }
}
